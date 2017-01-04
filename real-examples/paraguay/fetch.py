import optparse
import requests
import requests_cache
import json
import csv
from ratelimit import *

# Search, fetch records, fetch releases

@rate_limited(3)
def fetchData(id_list,folder,page=0):
    record_id = id_list[page]

    print("Fetching record " + str(page) + ' ID: ' + str(record_id) + " > https://www.contrataciones.gov.py:443/datos/api/v2/doc/ocds/record-package/"+ str(record_id))
    r = requests.get('https://www.contrataciones.gov.py:443/datos/api/v2/doc/ocds/record-package/' + str(record_id))

    try:
        with open(folder + '/'+ str(record_id) +".json","w",encoding='utf8') as release:
            release.write(json.dumps(r.json(),indent=2,ensure_ascii=False))
    except:
        with open("errors.txt",'a') as err:
            print("Failed to write "+ str(record_id))
            err.write('https://www.contrataciones.gov.py:443/datos/api/v2/doc/ocds/record-package/' + str(record_id) + "\n")

    page = int(page) + 1
    with open("page.n",'w') as n:
        n.write(str(page))

    if page < len(id_list):
        fetchData(id_list,folder,page)
    else:
        with open("page.n",'w') as n:
            n.write("0")


@rate_limited(1)
def fetchList(year):
    print("Fetching " + str(year) + " listing")
    r = requests.get('https://www.contrataciones.gov.py/images/opendata/planificaciones/' + str(year) + '.csv')
    print("Parsing")
    decoded_content = r.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    
    id_list = []

    for row in list(cr):
        id_list.append(row[2])

    return id_list[1:]

def main():

    requests_cache.install_cache('test_cache', backend='sqlite', expire_after=300)

    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)

    parser.add_option('-a','--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')

    parser.add_option('-R','--resume', action='store_true', default=False,
                      help='Continue from the last page (in page.n), for when download broken')

    parser.add_option('-y','--year', action='store', type="int", default=2016,
                      help='Which year to fetch activities from')

    (options, args) = parser.parse_args()


    id_list = fetchList(options.year)

    # id_list = [273637,273638,273639]

    if options.resume:
        with open("page.n",'r') as n:
            page = n.read()
    else:
        page = 0

    if options.all:
        fetchData(id_list,'all',int(page))
    else:
        id_list = id_list[:50]
        fetchData(id_list,'sample',int(page))

if __name__ == '__main__':
    main()