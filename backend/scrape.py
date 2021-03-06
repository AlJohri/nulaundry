import sys, time, requests, lxml.html
from pprint import pprint as pp

from blessings import Terminal
t = Terminal()

from firebase import firebase
firebase = firebase.FirebaseApplication('https://aljohri-nulaundry.firebaseio.com', None)

# http://m.laundryview.com/usage.php?lr=2025710

def scrape_locations():
    locations_url = "http://m.laundryview.com/lvs.php?s=328"
    locations_response = requests.get(locations_url)
    locations_doc = lxml.html.fromstring(locations_response.content)
    return [(location.get('id'), location.text) for location in locations_doc.cssselect("ul[data-role=listview] li:not([data-role=list-divider]) a")]

def scrape_machines():
    machines = {}
    for location_id, location_name in scrape_locations():
        # print location_name, location_id
        washers_dryers_url = "http://m.laundryview.com/submitFunctions.php?monitor=true&lr=%s&cell=null" % location_id
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
            machines[washer_id] = {
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
            machines[dryer_id] = {
                "location_id": location_id,
                "location_name": location_name,
                "id": dryer_id,
                "index": dryer_index,
                "status": dryer_status,
                "type": "dryer"
            }

    return machines

def save_locations():
    for location_id, location_name in scrape_locations():
        location = {"id": location_id, "name": location_name}
        print location
        firebase.put(url='/locations', name=location_id, data=location, headers={'print': 'pretty'})

def save_machines():
    for machine_id, machine in scrape_machines().iteritems():
        if machine['status'] != "Out of service": del machine['status']
        print machine
        firebase.put(url='/machines', name=machine_id, data=machine, headers={'print': 'pretty'})

def save_statuses():
    while True:

        timestamp = int(time.time() * 1000)

        for machine_id, machine in scrape_machines().iteritems():

            last = firebase.get(url="/machines/%s/statuses" % machine_id, name=None) # params={"limitToLast": 1}
            last_array = sorted(last.values(), key=lambda x: x[0]) if last else []
            last_timestamp, last_status = last_array[-1] if last else ("", "")

            status = machine.pop('status')
            if status == "Out of service": continue

            if last_status != status:
                firebase.put(url='/machines/%s/statuses' % machine_id, name=timestamp, data=(timestamp, status), headers={'print': 'pretty'})
                firebase.put(url='/machines/%s' % machine_id, name='timestamp', data=timestamp, headers={'print': 'pretty'})
                firebase.put(url='/machines/%s' % machine_id, name='status', data=status, headers={'print': 'pretty'})
                print machine_id, t.red(last_status), "=>", t.green(status)

                if status == "Avail":

                    all_avails = [tm for tm,st in last_array[:-1] if st == "Avail" and tm < timestamp] if last else None

                    last_avail_timestamp = all_avails[-1] if all_avails else None
                    last_avail_timestamp_index = last_array.index([last_avail_timestamp, "Avail"]) if last_avail_timestamp else None
                    timestamp_after_last_avail = last_array[last_avail_timestamp_index + 1][0] if last_avail_timestamp_index else None

                    if timestamp_after_last_avail:
                        prev_num_runs = firebase.get(url='/machines/%s' % machine_id, name='num_runs', headers={'print': 'pretty'}) or 0
                        firebase.put(url='/machines/%s' % machine_id, name='num_runs', data=prev_num_runs+1, headers={'print': 'pretty'})
                        firebase.post(url='/machines/%s/runs' % machine_id, data=(timestamp_after_last_avail, timestamp), headers={'print': 'pretty'})
                        print machine_id, "Run Complete:", timestamp_after_last_avail, timestamp

        print "\nSleeping 10 seconds ...\n"

if __name__ == '__main__':

    if len(sys.argv) != 2:
        raise Exception("Usage: python scrape.py <resource>")

    if sys.argv[1] == "statuses":
        save_statuses()
    elif sys.argv[1] == "machines":
        save_machines()
    elif sys.argv[1] == "locations":
        scrape_locations()
