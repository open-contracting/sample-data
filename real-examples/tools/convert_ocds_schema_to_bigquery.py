import json
from pprint import pprint

'''
Transform the OCDS release schema to the format
required by Google BigQuery.
'''


def process_field(name, field, required):
    '''
    Given a field definition in the OCDS schema, process
    it into BigQuery schema format.
    '''
    print('\n-------\n' + name)
    if 'type' in field:
        print('input type:', field['type'])
    if 'format' in field:
        print('input format:', field['format'])

    # Get the mode. We overwrite this with the 'repeated' mode
    # for applicable types, see below.
    # For ease, make everything nullable.
    d = {
        'name': name,
        'mode': 'nullable'
    }

    # Get the type.
    if 'type' in field:
        prop_type = field['type']
        if isinstance(prop_type, list):
            # Handle mixed string/integer fields: we want to treat
            # these as strings, for extra flexibility.
            if 'string' in prop_type:
                d['type'] = 'string'
            else:
                d['type'] = prop_type[0]
        else:
            d['type'] = prop_type
        if 'format' in field and field['format'] == 'date-time':
            d['type'] = 'timestamp'
        if d['type'] == 'array':
            print('array prop_type')
            d['mode'] = 'repeated'
            if 'type' in field['items']:
                d['type'] = field['items']['type']
            else:
                d['type'] = 'record'
            print(d['type'])
        # BigQuery only allows for integers and floats. Cast all to float.
        if d['type'] == 'number':
            d['type'] = 'float'
        if d['type'] == 'object':
            d['type'] = 'record'
            # Recursively process child properties, if they exist.
            d['fields'] = []
            if 'properties' in field:
                for p in field['properties']:
                    result = process_field(p, field['properties'][p], None)
                    if result:
                        d['fields'].append(result)
            elif 'items' in field:
                for p in field['items']['properties']:
                    result = process_field(
                        p, field['items']['properties'][p], None)
                    if result:
                        d['fields'].append(result)
            else:
                # These are extensions - ignore for now.
                print('returning None')
                return None

    else:
        d['type'] = 'record'

    print('output type:', d['type'])
    print('output mode:', d['mode'])

    # Check whether this is a reference field, in which case,
    # process the reference.
    reference = None
    if '$ref' in field:
        reference = field['$ref']
    elif ('items' in field and '$ref' in field['items']):
        reference = field['items']['$ref']
    if reference:
        reference = reference.replace('#/definitions/', '')
        d['type'] = 'record'
        if reference in reference_defs:
            d['fields'] = reference_defs[reference]['fields']
        else:
            print('%s not in references for %s' % (reference, name))
            return None
    pprint(d)
    return d


fname = 'release-schema.json'
f = open(fname, 'r')
schema = json.load(f)

# Process definitions first. Specify the order manually, because there is a
# complicated series of dependencies.
reference_defs = {}
ordered_defs = [
    'Value', 'Period', 'RelatedProcess', 'Address', 'ContactPoint',
    'Identifier', 'Classification', 'Amendment', 'Item', 'Organization',
    'OrganizationReference', 'Transaction', 'Budget', 'Document', 'Milestone',
    'Implementation', 'Contract', 'Award', 'Tender', 'Planning'
]
if 'definitions' in schema:
    definitions = schema['definitions']
    for d in ordered_defs:
        reference_defs[d] = process_field(d, definitions[d], None)

# with open('test-schema.json', 'w') as f:
#     json.dump(reference_defs['Tender']['fields'], f, indent=2)
with open('references.json', 'w') as f:
    json.dump(reference_defs, f, indent=2)
# sys.exit()

# Now process the properties.
props = schema['properties']
definition = []
required = schema['required']
for p in props:
    print('\n-----------')
    d = process_field(p, props[p], required)
    if d:
        definition.append(d)

# Add the fields that we insert during our transformation process.
definition.append({
    'name': 'validationErrors',
    'type': 'string',
    'mode': 'nullable'
})
definition.append({
    'name': 'version',
    'type': 'string',
    'mode': 'nullable'
})
definition.append({
    'name': 'packageInfo',
    'type': 'record',
    'mode': 'nullable',
    'fields': [
        {
            "type": "string",
            "name": "uri",
            "mode": "nullable"
        },
        {
            "type": "timestamp",
            "name": "publishedDate",
            "mode": "nullable"
        },
        {
            "type": "record",
            "name": "publisher",
            "mode": "nullable",
            "fields": [
                {
                    "type": "string",
                    "name": "name",
                    "mode": "nullable"
                },
                {
                    "type": "string",
                    "name": "scheme",
                    "mode": "nullable"
                },
                {
                    "type": "string",
                    "name": "uid",
                    "mode": "nullable"
                },
                {
                    "type": "string",
                    "name": "uri",
                    "mode": "nullable"
                }
            ]
        }
    ]
})
# Add special field for UK contracts.
# TODO: Get rid of this, for consistency - we should
# delete all fields not in the standard schema.
tender = None
for d in definition:
    if d['name'] == 'tender':
        tender = d
tender['fields'].append({
    'name': 'xClassifications',
    'type': 'record',
    'mode': 'nullable',
    'fields': [
        {
            'name': 'isSuitableForVco',
            'type': 'boolean',
            'mode': 'nullable'
        },
        {
            'name': 'isSuitableForSme',
            'type': 'boolean',
            'mode': 'nullable'
        },
        {
            'name': 'ojeuContractType',
            'type': 'string',
            'mode': 'nullable'
        }
    ]
})

with open('release-schema-bq.json', 'w') as f:
    json.dump(definition, f, indent=2)
