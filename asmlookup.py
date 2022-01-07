import requests
import json
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")

def rebuild_database():
    data_json = {}
    for i in range(3000,3010):
        r = requests.get('https://api.asrank.caida.org/v2/restful/asns/' + str(i))
        invalid_json = r.json()
        rjson_str = json.dumps(invalid_json).replace("'","\"")
        rjson = json.loads(rjson_str)

        try:
            data_json[rjson['data']['asn']['asn']] = rjson['data']['asn']
        except:
            print('ASN does not exist.')
            data_json[str(i)] = 'No ASN'
        try:
            location = geolocator.reverse(str(data_json[rjson['data']['asn']['asn']]['latitude'])+","+str(data_json[rjson['data']['asn']['asn']]['longitude']))
            address = location.raw['address']
            print(address)
            for k in address:
                data_json[rjson['data']['asn']['asn']][k] = address[k]
        except:
            print('No location')



    with open('asm_data.json', 'w', encoding = 'utf8') as ye:
        json.dump(data_json, ye)


def lookup(query):
    asn_pack = {}
    results = ''
    with open('asm_data.json', 'r') as data:
        json_content = data.read()
        asn = json.loads(json_content)
        for key in asn:
            for k in asn[key]:
                if asn[key][k] == query:
                    results += 'Location: ' + asn[key][k] + '\n'
                    with open('results.txt', 'w') as result_file:
                        result_file.write(results)


def main():
    running = True
    while running:
        print('\n\nWhat would you like to do?\n1. Rebuild Database\n2. Search for a company')
        ans = input()
        if ans == '1':
            print('Rebuilding database...\nMay take over 4 hours')
            rebuild_database()
        if ans == '2':
            running2 = True
            while running2:
                    query = input('Please enter your exact search query: ')
                    lookup(query)
                    input('Results written to file.\nPress enter to continue')
                    running2 = False

        else:
            print('Please enter option 1 or 2')

main()
