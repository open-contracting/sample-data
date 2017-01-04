import optparse
import requests
import json

# Search, fetch records, fetch releases

def fetchData(page,folder,maxpage=0):
    print("Fetching page " + str(page) + ' https://www.contractsfinder.service.gov.uk/Published/Notices/OCDS/Search?order=asc&page=' + str(page))
    r = requests.get('https://www.contractsfinder.service.gov.uk/Published/Notices/OCDS/Search?order=asc&page=' + str(page))

    try:
        if(maxpage > -1): 
            maxpage = r.json()['maxPage']
        for result in r.json()['results']:
            with open(folder + '/'+result['releases'][0]['id'] + ".json","w") as release:
                release.write(json.dumps(result,indent=2))
    except:
        with open("errors.txt",'a') as err:
            print("Failed to get "+ str(page))
            err.write('https://www.contractsfinder.service.gov.uk/Published/Notices/OCDS/Search?order=asc&page=' + str(page) + "\n")

    page = int(page) + 1
    with open("page.n",'w') as n:
        n.write(str(page))

    if page <= maxpage or int(maxpage) == 0:
        fetchData(page,folder)
    else:
        with open("page.n",'w') as n:
            n.write("1")


def main():
    usage = 'Usage: %prog [ --all --cont ]'
    parser = optparse.OptionParser(usage=usage)

    parser.add_option('-a','--all', action='store_true', default=False,
                      help='Fetch all records, rather than a small extract')

    parser.add_option('-R','--resume', action='store_true', default=False,
                      help='Continue from the last page (in page.n), for when download broken')

    parser.add_option('-p','--page', action='store', type="int", default=1,
                      help='Start from page n of the results')

    (options, args) = parser.parse_args()

    if options.resume:
        with open("page.n",'r') as n:
            page = n.read()
    else:
        page = options.page

    if options.all:
        fetchData(page,'all')
    else:
        fetchData(page,'sample',-1)

if __name__ == '__main__':
    main()