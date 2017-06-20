import glob
import hashlib
import json
import optparse
import sys
import traceback
from collections import OrderedDict
from copy import deepcopy


'''
Script to transform JSON in OCDS schema v1.0 to v1.1
'''


def generate_party(parties, org, role=[]):
    '''
    Update the parties array, returning an updated organisation
    reference block to use.
    '''
    try:
        # If we have a schema AND id, we can generate a suitable ID.
        if len(org['identifier']['id']) > 0:
            orgid = org['identifier']['id']
        else:
            raise Exception("No identifier was found")
        if len(org['identifier']['scheme']) > 2 and \
                len(org['identifier']['scheme']) < 20:
            scheme = org['identifier']['scheme']
        else:
            raise Exception("Schemes need to be between 2 and 20 characters")
        identifier = scheme + "-" + orgid
    except Exception as err:
        # Otherwise, generate an ID based on a hash of the
        # who organisation object.
        # ToDo: Check if we should do this from name instead.
        identifier = hashlib.md5(json.dumps(org).encode('utf8')).hexdigest()

    # Then check if this organisation was already in the parties array.
    if parties.get(identifier, False):
        name = parties.get(identifier).get('name', '')
        contact = parties.get(identifier).get('contactPoint', '')
        # If it is there, but the organisation name and contact point
        # doesn't match, we need to add a separate organisation entry
        # for this sub-unit or department.
        if not(name == org.get('name', '')) \
           or not(contact == org.get('contactPoint', '')):
            n = json.dumps(org.get('name', '')).encode('utf8')
            c = json.dumps(org.get('contactPoint', '')).encode('utf8')
            identifier += "-" + hashlib.md5(n + c).hexdigest()

    # Now fetch existing list of roles and merge.
    roles = parties.get(identifier, {}).get('roles', [])
    org['roles'] = list(set(roles + role))
    # And add the identifier to the organisation object
    # before adding/updating the parties object.
    org['id'] = identifier
    parties[identifier] = deepcopy(org)
    return {"id": identifier, "name": org.get('name', '')}


def upgrade_parties(release):
    parties = {}
    try:
        print('trying', release['buyer'])
        release['buyer'] = generate_party(parties, release['buyer'], ['buyer'])
    except Exception as err:
        pass
    try:
        release['tender']['procuringEntity'] = \
            generate_party(parties, release['tender']['procuringEntity'],
                           ['procuringEntity'])
    except Exception as err:
        pass
    try:
        for num, tenderer in enumerate(release['tender']['tenderers']):
            release['tender']['tenderers'][num] = \
                generate_party(parties, tenderer, ['tenderer'])
    except Exception as err:
        pass
    # Update award and contract suppliers
    try:
        for anum, award in enumerate(release['awards']):
            suppliers = release['awards'][anum]['suppliers']
            for snum, supplier in enumerate(suppliers):
                release['awards'][anum]['suppliers'][snum] = \
                    generate_party(parties, supplier, ['supplier'])
    except Exception as err:
        pass
    # (Although contract suppliers is not in the standard, some
    # implementations have been using this.)
    try:
        for anum, award in enumerate(release['contracts']):
            suppliers = release['contracts'][anum]['suppliers']
            for snum, supplier in enumerate(suppliers):
                release['contracts'][anum]['suppliers'][snum] = \
                    generate_party(parties, supplier, ['supplier'])
    except Exception as err:
        pass

    # Now format the parties into a simple array
    release['parties'] = []
    for key in parties:
        release['parties'].append(parties[key])

    return release


def upgrade_transactions(release):
    try:
        for contract in release['contracts']:
            for transaction in contract['implementation']['transactions']:
                payer_id = transaction['providerOrganization']['scheme']\
                     + "-" + transaction['providerOrganization']['id']
                transaction['payer'] = {
                    "id": payer_id,
                    "name": transaction['providerOrganization']['legalName']
                }
                payee_id = transaction['receiverOrganization']['scheme']\
                    + "-" + transaction['receiverOrganization']['id']
                transaction['payee'] = {
                    "id": payee_id,
                    "name": transaction['receiverOrganization']['legalName']
                    }
                transaction['value'] = transaction['amount']
                del(transaction['providerOrganization'])
                del(transaction['receiverOrganization'])
                del(transaction['amount'])
    except Exception as e:
        # traceback.print_tb(e.__traceback__)
        pass

    return release


def upgrade(release):
    release = upgrade_parties(release)
    release = upgrade_transactions(release)
    release.move_to_end('parties', last=False)
    release.move_to_end('initiationType', last=False)
    release.move_to_end('tag', last=False)
    release.move_to_end('language', last=False)
    release.move_to_end('date', last=False)
    release.move_to_end('id', last=False)
    release.move_to_end('ocid', last=False)
    return release


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-f', '--filepath', action='store', default=None,
                      help='Path to files, e.g. paraguay/sample')
    (options, args) = parser.parse_args()
    if not options.filepath:
        parser.error('You must supply a filepath, using the -f argument')
    print('%s.json' % options.filepath)
    for filename in glob.glob('%s/*.json' % options.filepath):
        if not filename.endswith('.json'):
            print('Skipping non-JSON file %s' % filename)
            continue
        try:
            with open(filename, 'r') as file:
                data = json.loads(file.read(), object_pairs_hook=OrderedDict)
                data.update({"version": "1.1"}),
                data['extensions'] = []
                if 'releases' in data:
                    data.move_to_end('releases', last=True)
                    for release in data['releases']:
                        release = upgrade(release)
                else:
                    print('Releases property missing, not updating')
                with open(filename, 'w') as writefile:
                    writefile.write(json.dumps(data, indent=2))
        except Exception as e:
            print("Problem updating " + filename)
            print(e)

if __name__ == '__main__':
    main()
