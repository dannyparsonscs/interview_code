#Danny Parsons Interview Coding Challenge

## Instructions
1. Get XML from API: https://www.senate.gov/general/contact_information/senators_cfm.xml
1. For the data contained inside the M​ember​ fields in the XML file, convert the data into
the JSON format listed below.​
  {
    “firstName”: “First”,
    “lastName”: “Last”,
    “fullName”: “First Last”,
    “chartId”: “:Contents of bioguide_id:”, “mobile”: “Phone”,
    “address”: [ {
    “street”: “123 Main Street”, “city”: “Orlando”,
    “state”: “FL”,
    “postal”: 32825
  ] }
1. Print the converted data.

## How To Run
1. Clone repo into a directory on a computer with Python 3.8 installed
1. CD into the directory with command terminal
1. Run 'python3 danny_parsons_test.py'

Console output is the JSON.


## Code
The code in danny_parsons_test.py is broken down into the following functions:
- get_xml_data(url): takes a URL and uses the python "requests" module to do a simple HTTP request
- get_senators(xml): takes the XML string and converts it into a list with the data for each senator
- format_senators(senators): cleans up various white space errors and uses a regular expression to pick apart relevant address details
- make_json(formatted_senators): list into JSON object
- main(): executes all four functions above and then prints the json

output.json has an example of the json formatted nicely for readability.

## Notes
- "Washington DC" is hardcoded as a capture group for the address regular expression because it was unanimous across each senator.
