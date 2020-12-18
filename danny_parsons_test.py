import requests
import json
import xml.etree.ElementTree as etree
import re

# extracts xml data and returns string content of xml
def get_xml_data(url):
    # headers required to get around blocks of web scraping
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}
    response = requests.get(url, headers=headers)
    #only send back if successful response, otherwise return error information
    if response.status_code == 200:
        return response.content
    else:
        return ("Unable to query " + url + "\nResponse Status Code: " + str(response.status_code))

def get_senators(xml):
    # using an element tree to iterate through
    tree = etree.fromstring(xml)

    # using these different lists to zip up each senator at the end
    firstnames = []
    lastnames = []
    chartIds = []
    phones = []
    addresses = []

    # iterating through list
    for child in tree.iter():
        if child.tag == "last_name":
            lastnames.append(child.text)
        elif child.tag == "first_name":
            firstnames.append(child.text)
        elif child.tag == "bioguide_id":
            chartIds.append(child.text)
        elif child.tag == "phone":
            phones.append(child.text)
        elif child.tag == "address":
            addresses.append(child.text)

    # zipping up so that senator tuples inside contain all relevant information
    senators = list(zip(firstnames, lastnames, chartIds, phones, addresses))
    # for ease later, turning tuples from zip into lists
    for index, senator in enumerate(senators):
        senators[index] = list(senator)

    return senators

def format_senators(senators):
    for senator in senators:
        # adding full name
        first = senator[0]
        last = senator[1]
        full_name = first + " " + last
        senator.insert(2, full_name)

        #stripping new line characters from address string
        stripped_address = senator[5].replace("\n", "")
        senator[5] = stripped_address

        # this admittedly uses the hardcoded "Washington DC" but because it is both city and "state"
        # and every senator's address has it, I thought this was acceptable
        address_regex = r'([A-Z]?[0-9]{,3}[A-Z]{,1} [a-zA-Z ]*) (Washington DC[\s]*) ([0-9]{5})'
        address_pattern = re.compile(address_regex)
        address_matches = re.findall(address_pattern, senator[5])

        street = address_matches[0][0]
        city = address_matches[0][1]
        state = city
        postal = address_matches[0][2]

        # turning address into a list to make nesting the objects easier
        address = [street.strip(), city.strip(), state.strip(), postal.strip()]
        senator[5] = address

    return senators

# turns our list of formatted string into the right json format
def make_json(senators):
    senators_list = []

    #formatting the json as specified
    for senator in senators:
        senator_json = {
            "firstName": senator[0],
            "lastName": senator[1],
            "fullName": senator[2],
            "chartId": senator[3],
            "mobile": senator[4],
            "address": [
                {
                    #removing leftover whitespace from xml parsing
                    "street": senator[5][0],
                    "city": senator[5][1],
                    "state": senator[5][2],
                    "postal": senator[5][3],
                }
            ]
        }

        # senators_list = senators_list + senator_json
        senators_list.append(senator_json)

    senators_json = json.dumps(senators_list)
    return senators_json


def main():
    xml = get_xml_data("https://www.senate.gov/general/contact_information/senators_cfm.xml")
    senators = get_senators(xml)
    formatted_senators = format_senators(senators)
    json_data = make_json(formatted_senators)
    print(json_data)

if __name__ == "__main__":
    main()