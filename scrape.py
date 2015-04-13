import time, requests, lxml.html
from pprint import pprint as pp

from blessings import Terminal
t = Terminal()

def scrape_laundryview():

    items = {}

    locations_url = "http://m.laundryview.com/lvs.php?s=328"
    locations_response = requests.get(locations_url)
    locations_doc = lxml.html.fromstring(locations_response.content)

    for location in locations_doc.cssselect("ul[data-role=listview] li:not([data-role=list-divider]) a"):
        location_name = location.text
        location_id = location.get('id')

        # print location_name, location_id

        washers_dryers_url = "http://m.laundryview.com/submitFunctions.php?monitor=true&lr=%s&cell=null" % location.get('id')
        washers_dryers_response = requests.get(washers_dryers_url)
        washers_dryers_doc = lxml.html.fromstring(washers_dryers_response.content)

        washer = washers_dryers_doc.cssselect("#washer")[0]
        while True:
            washer = washer.getnext()
            if washer is None or washer.get('id') != None: break
            washer_index = [x for x in washer.itertext()][0].strip()
            washer_status = washer.cssselect('a:nth-child(1) p')[0].text
            washer_id = washer.cssselect('a')[0].get('id')
            # print "\t", "washer", washer_id, washer_index, washer_status
            items[washer_id] = {
                "location_id": location_id,
                "location_name": location_name,
                "id": washer_id,
                "index": washer_index,
                "status": washer_status,
                "type": "washer"
            }

        dryer = washers_dryers_doc.cssselect("#dryer")[0]
        while True:
            dryer = dryer.getnext()
            if dryer is None or dryer.get('id') != None: break
            dryer_index = [x for x in dryer.itertext()][0].strip()
            dryer_status = dryer.cssselect('a:nth-child(1) p')[0].text
            dryer_id = dryer.cssselect('a')[0].get('id')
            # print "\t", "dryer", dryer_id, dryer_index, dryer_status
            items[dryer_id] = {
                "location_id": location_id,
                "location_name": location_name,
                "id": dryer_id,
                "index": dryer_index,
                "status": dryer_status,
                "type": "dryer"
            }

    return items

if __name__ == '__main__':

    from firebase import firebase
    firebase = firebase.FirebaseApplication('https://aljohri-nulaundry.firebaseio.com', None)

    previous = {}
    current = {}
    while True:
        previous = current
        current = scrape_laundryview()

        for item_id, item in current.iteritems():

            if previous == {} or previous[item_id]['status'] != current[item_id]['status']:
                current[item_id]['timestamp'] = int(time.time())
                key = "%s-%s" % (item_id, current[item_id]['timestamp'])
                result = firebase.put(url='/status', name=key, data=current[item_id], headers={'print': 'pretty'})

                if previous == {}:
                    print item_id, t.red("NA"), "=>", t.green(current[item_id]['status'])
                else:
                    print item_id, t.red(previous[item_id]['status']), "=>", t.green(current[item_id]['status'])

        print "\nSleeping 10 seconds ...\n"
