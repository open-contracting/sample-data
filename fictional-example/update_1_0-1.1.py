from copy import deepcopy
import hashlib
import json
import glob
from collections import OrderedDict

# Update the parties array and return an updated organisation reference block to use.


def generate_party(parties, org, role=[]):

    # If we have a schema AND id, we can generate a suitable ID
    try:
        if len(org['identifier']['id']) > 0:
            orgid = org['identifier']['id']
        else:
            raise Exception("No identifier was found")

        if len(org['identifier']['scheme']) > 2 and len(org['identifier']['scheme']) < 20:
            scheme = org['identifier']['scheme']
        else:
            raise Exception("Schemes need to be between 2 and 20 characters")

        identifier = scheme + "-" + orgid

    # Otherwise we generate an ID based on a hash of the who organisation object
    # ToDo: Check if we should do this from name instead...
    except Exception as err:
        identifier = hashlib.md5(json.dumps(org).encode('utf8')).hexdigest()

    # Then we check if this organisation was already in the parties array
    if parties.get(identifier, False):
        # If it is there, but the organisation name and contact point doesn't match, we need to add a separate
        # organisation entry for this sub-unit or department
        if not(parties.get(identifier).get('name', '') == org.get('name', '')) or not(parties.get(identifier).get('contactPoint', '') == org.get('contactPoint', '')):  # noqa
            identifier = identifier + "-" + hashlib.md5(json.dumps(org.get('name', '')).encode(
                'utf8') + json.dumps(org.get('contactPoint', '')).encode('utf8')).hexdigest()

    # Now we fetch existing list of roles and merge
    roles = parties.get(identifier, {}).get('roles', [])
    org['roles'] = list(set(roles + role))

    # And we add the identifier to the organisation object before adding/updated the parties object
    org['id'] = identifier
    parties[identifier] = deepcopy(org)

    return {"id": identifier, "name": org.get('name', '')}


def upgrade_parties(release):
    parties = {}

    # Update procuringEntity
    try:
        release['buyer'] = generate_party(parties, release['buyer'], ['buyer'])
    except Exception as err:
        pass

    # Update procuringEntity
    try:
        release['tender']['procuringEntity'] = generate_party(
            parties, release['tender']['procuringEntity'], ['procuringEntity'])
    except Exception as err:
        pass

    # Update tenderers
    try:
        for num, tenderer in enumerate(release['tender']['tenderers']):
            release['tender']['tenderers'][num] = generate_party(parties, tenderer, ['tenderer'])
    except Exception as err:
        pass

    # Update award and contract suppliers
    try:
        for anum, award in enumerate(release['awards']):
            for snum, supplier in enumerate(release['awards'][anum]['suppliers']):
                release['awards'][anum]['suppliers'][snum] = generate_party(parties, supplier, ['supplier'])
    except Exception as err:
        pass

    # (Although contract suppliers is not in the standard, some implementations have been using this)
    try:
        for anum, award in enumerate(release['contracts']):
            for snum, supplier in enumerate(release['contracts'][anum]['suppliers']):
                release['contracts'][anum]['suppliers'][snum] = generate_party(parties, supplier, ['supplier'])
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
                transaction['payer'] = {
                    "id": transaction['providerOrganization']['scheme'] + "-" +
                    transaction['providerOrganization']['id'],
                    "name": transaction['providerOrganization']['legalName'],
                }
                transaction['payee'] = {
                    "id": transaction['receiverOrganization']['scheme'] + "-" +
                    transaction['receiverOrganization']['id'],
                    "name": transaction['receiverOrganization']['legalName'],
                }
                transaction['value'] = transaction['amount']
                del(transaction['providerOrganization'])
                del(transaction['receiverOrganization'])
                del(transaction['amount'])
    except Exception as e:
        # traceback.print_tb(e.__traceback__)
        pass

    return release


# Expects a JSON object containing a release
def upgrade(release):
    # First, create the parties array.
    release = upgrade_parties(release)
    release = upgrade_transactions(release)

    # Now sort out the odering
    release.move_to_end('parties', last=False)
    release.move_to_end('initiationType', last=False)
    release.move_to_end('tag', last=False)
    release.move_to_end('language', last=False)
    release.move_to_end('date', last=False)
    release.move_to_end('id', last=False)
    release.move_to_end('ocid', last=False)
    return release


for filename in glob.glob("*.json"):
    try:
        with open(filename, 'r') as file:
            data = json.loads(file.read(), object_pairs_hook=OrderedDict)
            data.update({"version": "1.1"}),
            data['extensions'] = []
            data.move_to_end('releases', last=True)
            for release in data['releases']:
                release = upgrade(release)

        with open(filename, 'w') as writefile:
            writefile.write(json.dumps(data, indent=2))
    except Exception as e:
        print(e)
        print("Problem updating " + filename)
        pass
