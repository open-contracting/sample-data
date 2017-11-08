import glob
import json
import optparse
import re
from datetime import datetime

from __builtin__ import unicode
from jsonschema import Draft3Validator

'''
Given a set of OCDS releases, fix problems that will stop them loading
into BigQuery.
Currently this file does the following:
- Converts ID fields that are integers to string values
- Converts date formats to those expected by BigQuery
- Automatically removes additional fields in publisher files
- Manually fixes various non-schema-compliant fields in publisher files
- Prints converted data to a newline-delimited JSON output file.
'''


def ids_to_string(mydict):
    '''
    Recursively make all IDs strings. This is because IDs in the
    OCDS definition can be either integers or strings, but
    BigQuery can't cope with mixed types.
    '''
    for k, v in mydict.items():
        if k == 'id' and type(v) is int or type(v) is float:
            mydict[k] = str(v)
        elif type(v) is dict:
            mydict[k] = ids_to_string(mydict[k])
        elif type(v) is list:
            for i, item in enumerate(v):
                if type(v[i]) is dict:
                    v[i] = ids_to_string(v[i])
    return mydict


def fix_date_formats(mydict):
    '''
    Recursively fix date formats - this is a problem for the
    Canada "buyandsell" publisher.
    '''
    for k, v in mydict.items():
        if k == 'date' or k == 'startDate' \
                or k == 'endDate' or k == 'awardDate':
            if mydict[k]:
                try:
                    d = datetime.strptime(
                        mydict[k], "%Y-%m-%d")
                    mydict[k] = \
                        datetime.strftime(d, "%Y-%m-%d %H:%M")
                except ValueError:
                    pass
                except TypeError:
                    pass
        elif type(v) is dict:
            mydict[k] = fix_date_formats(mydict[k])
        elif type(v) is list:
            for i, item in enumerate(v):
                if type(v[i]) is dict:
                    v[i] = fix_date_formats(v[i])
    return mydict


def fix_uk_issues(data):
    '''
    Fix minor mis-naming issue, plus missing and null tags.
    '''
    if 'parties' in data:
        for p in data['parties']:
            if 'contactPoint' in p:
                if 'uri' in p['contactPoint']:
                    p['contactPoint']['url'] = p['contactPoint']['uri']
                    del p['contactPoint']['uri']
        if 'tag' not in data:
            data['tag'] = []
        if len(data['tag']) == 1 and not data['tag'][0]:
            data['tag'] = []
    return data


def fix_mexico_grupo_issues(data):
    '''
    Remove extra field.
    NB: It's possible the manual deletion of extra keys
    is no longer required, now we have the jsonschema step.
    '''
    if 'tender' in data:
        if 'metodoDeAdquisicion' in data['tender']:
            del data['tender']['metodoDeAdquisicion']
    return data


def fix_mexico_cdmx_issues(data):
    '''
    Remove extra fields, iteratively.
    NB: It's possible the manual deletion of extra keys
    is no longer required, now we have the jsonschema step.
    '''
    for k, v in data.items():
        forbidden = [
            'dateexchangeRate', 'amountyear', 'multiYear',
            'valueyear', 'exchangeRate']
        if k in forbidden:
            del data[k]
        elif type(v) is dict:
            data[k] = fix_mexico_cdmx_issues(data[k])
        elif type(v) is list:
            for i, item in enumerate(v):
                if type(v[i]) is dict:
                    v[i] = fix_mexico_cdmx_issues(v[i])
    return data


def fix_moldova_issues(data):
    '''
    Fix typo'd field name.
    '''
    if 'tender' in data:
        if 'numberOfTenders' in data['tender']:
            data['tender']['numberOfTenderers'] = \
                data['tender']['numberOfTenders']
            del data['tender']['numberOfTenders']
    return data


def fix_nsw_issues(data):
    '''
    Remove extra keys, fix string formatting.
    NB: It's possible the manual deletion of extra keys
    is no longer required, now we have the jsonschema step.
    '''
    permitted_tender_keys = [
        u'procurementMethod', u'amendment',
        u'awardPeriod', u'mainProcurementCategory', u'enquiryPeriod',
        u'minValue', u'numberOfTenderers', u'value', u'tenderers',
        u'id', u'description', u'amendments', u'documents', u'title',
        u'awardCriteria', u'procurementMethodRationale', u'contractPeriod',
        u'status', u'eligibilityCriteria', u'tenderPeriod',
        u'procurementMethodDetails', u'additionalProcurementCategories',
        u'submissionMethod', u'milestones', u'submissionMethodDetails',
        u'items', u'awardCriteriaDetails', u'hasEnquiries', u'procuringEntity'
    ]
    forbidden_keys = []
    if 'tender' in data:
        for k in data['tender']:
            if k not in permitted_tender_keys:
                forbidden_keys.append(k)
    for f in forbidden_keys:
        del data['tender'][f]
        if 'amendment' in data['tender'] and \
                        'changes' in data['tender']['amendment']:
            for c in data['tender']['amendment']['changes']:
                if 'former_value' in c \
                        and type(c['former_value']) is not str:
                    c['former_value'] = str(c['former_value'])
    if 'awards' in data:
        for a in data['awards']:
            if 'CNUUID' in a:
                del a['CNUUID']
            if 'valueDescription' in a:
                del a['valueDescription']
            if 'title' in a and \
                    (type(a['title']) is int or type(a['title']) is float):
                a['title'] = str(a['title'])

    return data


def fix_taiwan_issues(data):
    '''
    Fix extra fields, fix packageInfo publisher
    and date fields.
    '''
    if 'awards' in data and isinstance(data['awards'], dict):
        data['awards'] = [data['awards']]
        for a in data['awards']:
            # I don't understand why jsonschema isn't picking up
            # these extra fields - additionalProperties is set
            # to false on awards and items. Anyway, delete them.
            extra_fields = ['awardAnnounceDate', 'totalAwardValue',
                            'awardCriteria', 'awardDate']
            for e in extra_fields:
                if e in a:
                    del a[e]
            if 'items' in a:
                for i in a['items']:
                    extra_fields = ['withoutTenderer', 'suppliers', 'number']
                    for e in extra_fields:
                        if e in i:
                            del i[e]
    if 'pageageInfo' in data:
        if isinstance(data['packageInfo']['publisher'], str):
            name = data['packageInfo']['publisher']
            data['packageInfo']['publisher'] = {
                'name': name
            }
    if 'packageInfo' in data and 'publishedDate' in data['packageInfo']:
        try:
            d = datetime.strptime(
                data['packageInfo']['publishedDate'], "%Y-%m-%d")
            data['packageInfo']['publishedDate'] = \
                datetime.strftime(d, "%Y-%m-%d %H:%M")
        except (ValueError, TypeError) as e:
            pass
    return data


def fix_nigeria_issues(data):
    '''
    Fix date format.
    '''
    if 'packageInfo' in data and 'publishedDate' in data['packageInfo']:
        try:
            d = datetime.strptime(
                data['packageInfo']['publishedDate'], "%Y-%m-%dT%H:%M:%SZ")
            data['packageInfo']['publishedDate'] = \
                datetime.strftime(d, "%Y-%m-%d %H:%M")
        except (ValueError, TypeError) as e:
            pass
    return data


def fix_colombia_issues(data):
    '''
    Fix a one-off formatting error.
    '''
    if 'planning' in data and 'budget' in data['planning']:
        budget = data['planning']['budget']
        if 'amount' in budget and 'amount' in budget['amount']:
            amount = budget['amount']['amount']
            if amount and type(amount) == str and amount.strip() == "450.000.000":
                budget['amount']['amount'] = 450000000
    return data


def fix_montreal_issues(data):
    '''
    Fix tags: they should be arrays, not strings.
    '''
    if 'tag' in data and isinstance(data['tag'], str):
        data['tag'] = [data['tag']]
    return data


def fix_mexico_inai_issues(data):
    '''
    Fix data types issues.
    '''
    if 'parties' in data:
        for p in data['parties']:
            if 'additionalIdentifiers' in p:
                if 'uri' in p['additionalIdentifiers'] and isinstance(p['additionalIdentifiers']['uri'], int):
                    p['additionalIdentifiers']['uri'] = str(p['additionalIdentifiers']['uri'])
            if 'address' in p:
                if 'postalCode' in p['address'] and isinstance(p['address']['postalCode'], int):
                    p['address']['postalCode'] = str(p['address']['postalCode'])
            if 'contactPoint' in p:
                if 'telephone' in p['contactPoint'] and isinstance(p['contactPoint']['telephone'], int):
                    p['contactPoint']['telephone'] = str(p['contactPoint']['telephone'])
    if 'tender' in data:
        if 'minValue' in data['tender'] and 'amount' in data['tender']['minValue'] and isinstance(
                data['tender']['minValue']['amount'], unicode):
            try:
                data['tender']['minValue']['amount'] = float(data['tender']['minValue']['amount'])
            except:
                data['tender']['minValue']['amount'] = None
        if 'submissionMethod' in data['tender'] and isinstance(data['tender']['submissionMethod'], unicode):
            data['tender']['submissionMethod'] = [data['tender']['submissionMethod']]
        if 'additionalProcurementCategories' in data['tender'] \
                and type(data['tender']['additionalProcurementCategories']) == unicode:
            data['tender']['additionalProcurementCategories'] = [data['tender']['additionalProcurementCategories']]
        if 'awardPeriod' in data['tender'] and 'durationInDays' in data['tender']['awardPeriod'] and \
                isinstance(data['tender']['awardPeriod']['durationInDays'], unicode):
            try:
                data['tender']['awardPeriod']['durationInDays'] = int(data['tender']['awardPeriod']['durationInDays'])
            except:
                data['tender']['awardPeriod']['durationInDays'] = None
        if 'awardPeriod' in data['tender'] and 'maxExtentDate' in data['tender']['awardPeriod'] \
                and (isinstance(data['tender']['awardPeriod']['maxExtentDate'], int)
                     or data['tender']['awardPeriod']['maxExtentDate'] == 'n/a'
                     or data['tender']['awardPeriod']['maxExtentDate'] == '-'):
            data['tender']['awardPeriod']['maxExtentDate'] = None
        if 'awardPeriod' in data['tender'] and 'startDate' in data['tender']['awardPeriod'] and \
                        data['tender']['awardPeriod']['startDate'] == 'No palica':
            data['tender']['awardPeriod']['startDate'] = None
        if 'documents' in data['tender']:
            for p in data['tender']['documents']:
                if 'dateModified' in p and (p['dateModified'] == 'n/a' or p['dateModified'] == 'No aplica \n' or
                                                    p['dateModified'] == 'No palica'):
                    p['dateModified'] = None
        if 'tenderPeriod' in data['tender'] and 'maxExtentDate' in data['tender']['tenderPeriod']:
            try:
                datetime.strptime(data['tender']['tenderPeriod']['maxExtentDate'], '%YYYY-%mm-%dd')
            except ValueError:
                data['tender']['tenderPeriod']['maxExtentDate'] = None
        if 'tenderPeriod' in data['tender'] and 'endDate' in data['tender']['tenderPeriod'] and \
                        data['tender']['tenderPeriod']['endDate'] == '20/12/2016.':
            data['tender']['tenderPeriod']['endDate'] = '2016-12-20 00:00'
    if 'planning' in data and 'documents' in data['planning']:
        for p in data['planning']['documents']:
            if 'dateModified' in p and p['dateModified'] == 'n/a':
                p['dateModified'] = None
    if 'awards' in data:
        for p in data['awards']:
            if 'contractPeriod' in p and 'maxExtentDate' in p['contractPeriod'] \
                    and (isinstance(p['contractPeriod']['maxExtentDate'], int)
                         or p['contractPeriod']['maxExtentDate'] == 'n/a'):
                p['contractPeriod']['maxExtentDate'] = None
            if 'documents' in p:
                for pp in p['documents']:
                    if 'datePublished' in pp and pp['datePublished'] == 'n/a':
                        pp['datePublished'] = None
                    if 'dateModified' in pp and pp['dateModified'] == 'n/a':
                        pp['dateModified'] = None
            if 'items' in p:
                for pp in p['items']:
                    if 'classification' in pp and 'uri' in pp['classification'] \
                            and isinstance(pp['classification']['uri'], int):
                        pp['classification']['uri'] = str(pp['classification']['uri'])
            if 'date' in p:
                try:
                    datetime.strptime(p['date'], '%YYYY-%mm-%dd')
                except ValueError:
                    p['date'] = None

    if 'contracts' in data:
        for p in data['contracts']:
            if 'period' in p and 'maxExtentDate' in p['period'] \
                    and (isinstance(p['period']['maxExtentDate'], int)
                         or p['period']['maxExtentDate'] == 'n/a'):
                p['period']['maxExtentDate'] = None
            if 'documents' in p:
                for pp in p['documents']:
                    if 'dateModified' in pp:
                        try:
                            datetime.strptime(pp['dateModified'], '%YYYY-%mm-%dd')
                        except ValueError:
                            pp['dateModified'] = None
    return data


def remove_extra_fields(data, schema, IS_VERBOSE):
    '''
    Delete extra fields reported by jsonschema.
    This is pretty inelegant, and jsonschema is a bit unpredictable
    about what it reports, see e.g. https://goo.gl/yCNGMw
    I think personally I'd ditch this code and just delete
    fields manually, given that (a) it's actually helpful to examine
    what publishers have supplied - often they just misname fields,
    which can usefully be renamed rather than deleted (b) almost
    always, other manual tweaks are required to get the data into shape,
    so it's never going to be a fully automated process anyway
    (c) there aren't many publishers, so it's not much of an overhead.
    '''
    has_extra_fields = False
    v = Draft3Validator(schema)
    errors = sorted(v.iter_errors(data), key=str)
    for error in errors:
        temp = data
        error_path = error.absolute_schema_path

        # Ignore all errors apart from extra properties.
        if error_path[-1] == 'additionalProperties':
            has_extra_fields = True
            # Hacky way to get property names, but seems to be
            # the best offered by jsonschema.
            unwanted_properties = re.findall(r"'(\w+)'", error.message)
            path_expression = []
            for i, e in enumerate(error_path):
                if e == 'additionalProperties':
                    continue
                if e == 'properties':
                    i += 1
                    path_expression.append(error_path[i])
            if IS_VERBOSE:
                print('\nJSONSchema raw error path: %s' % error_path)
                print('Processed error path: %s' % path_expression)
                print('Unwanted properties: %s' % unwanted_properties)

            # We now have details of the unwanted properties: remove them
            # from the data object.
            # First retrieve the relevant part of the data. We can't predict
            # whether this will be a dict or a list.
            for p in path_expression:
                if p in temp:
                    temp = temp[p]
                elif isinstance(temp, list):
                    temp_x = []
                    for t in temp:
                        if isinstance(t, dict) and p in t:
                            temp_x.append(t[p])
                    if temp_x:
                        temp = temp_x
            # Now iterate over the relevant part of the data, and remove
            # the unwanted property.
            if isinstance(temp, list):
                # Flatten lists of lists.
                if any(isinstance(el, list) for el in temp):
                    flat_list = [item for sublist in temp for item in sublist]
                    temp = flat_list
                for d in temp:
                    for unwanted_property in unwanted_properties:
                        if unwanted_property in d:
                            del d[unwanted_property]
                        else:
                            t = None
                            # Use the last property in the path if required.
                            if path_expression[-1] in d:
                                t = d[path_expression[-1]]
                            elif len(path_expression) > 1 and \
                                            path_expression[-2] in d and \
                                            path_expression[-1] in \
                                            d[path_expression[-2]]:
                                t = d[path_expression[-2]][path_expression[-1]]
                            if isinstance(t, list):
                                for s in t:
                                    if unwanted_property in s:
                                        del s[unwanted_property]
                            elif t:
                                if unwanted_property in t:
                                    del t[unwanted_property]
            else:
                for unwanted_property in unwanted_properties:
                    if unwanted_property in temp:
                        del temp[unwanted_property]

    return data, has_extra_fields


def add_additionalProperties_to_schema(schema_obj):
    '''
    We need to remove any fields not explicitly listed in the schema,
    because BigQuery can't cope with extra fields.
    To do this, we specify additionalProperties=false explicitly
    on every object. Walk the schema and add this property to every object.
    '''
    if 'type' in schema_obj and schema_obj['type'] == 'object':
        schema_obj['additionalProperties'] = False
        # Remove patternProperties, as it seems to interact badly with
        # additionalProperties: https://goo.gl/yCNGMw
        if 'patternProperties' in schema_obj:
            del schema_obj['patternProperties']
        # Handle the special case of definitions,
        # which don't have the "type: object" property.
        if 'definitions' in schema_obj:
            for d in schema_obj['definitions']:
                add_additionalProperties_to_schema(
                    schema_obj['definitions'][d])
        props = schema_obj['properties']
        for p in props:
            add_additionalProperties_to_schema(props[p])
    return schema_obj


def add_permitted_values(schema):
    '''
    We have added some useful properties to our data that aren't in the
    OCDS schema. Add these explicitly here so they don't get deleted.
    '''
    schema['properties']['version'] = {"type": "string"}
    schema['properties']['validationErrors'] = {"type": "string"}
    schema['properties']['packageInfo'] = {
        "type": "object",
        "properties": {
            "uri": {"type": "string"},
            "publishedDate": {"type": "string"},
            "publisher": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "scheme": {"type": "string"},
                    "uri": {"type": "string"},
                    "uid": {"type": "string"}
                }
            }
        }
    }
    return schema


def treat_record_as_release(data):
    '''
    When we are dealing with a record, for now we just take the compiledRelease
    and upload this to bigQuery.
    '''
    if 'compiledRelease' in data:
        return data['compiledRelease']
    else:
        return data


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-f', '--filepath', action='store', default=None,
                      help='Path to files, e.g. parguay/sample')
    parser.add_option('-V', '--verbose', action='store_true', default=False,
                      help='Print verbose output')
    (options, args) = parser.parse_args()
    if not options.filepath:
        parser.error('You must supply a filepath, using the -f argument')

    all_data = []
    files = glob.glob('%s*' % options.filepath)
    schema = json.load(open('release-schema.json'))
    schema = add_permitted_values(schema)
    schema = add_additionalProperties_to_schema(schema)
    # with open('schema_with_additionalproperties.json', 'w') as outfile:
    #     json.dump(schema, outfile)
    for i, filename in enumerate(files):
        if options.verbose:
            print(filename)
        if not i % 1000:
            print('Processing file %s of %s' % (i, len(files)))
        if not filename.endswith('.json'):
            print('Skipping non-JSON file %s' % filename)
            continue
        with open(filename, 'r') as file:
            try:
                data = json.load(file)
            except Exception as e:
                print('Problem loading', filename)
                print(e)
                continue
            data = treat_record_as_release(data)
            has_extra_fields = True
            while has_extra_fields:
                data, has_extra_fields = remove_extra_fields(
                    data, schema, options.verbose)
            data = ids_to_string(data)
            data = fix_date_formats(data)
            data = fix_uk_issues(data)
            data = fix_mexico_grupo_issues(data)
            data = fix_mexico_cdmx_issues(data)
            data = fix_moldova_issues(data)
            data = fix_nsw_issues(data)
            data = fix_nigeria_issues(data)
            data = fix_montreal_issues(data)
            data = fix_taiwan_issues(data)
            data = fix_colombia_issues(data)
            data = fix_mexico_inai_issues(data)
        all_data.append(data)
    with open('all-releases.json', 'w') as writefile:
        for d in all_data:
            json.dump(d, writefile)
            writefile.write('\n')


if __name__ == '__main__':
    main()
