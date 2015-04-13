import requests, lxml.html

locations_url = "http://m.laundryview.com/lvs.php?s=328"
locations_response = requests.get(locations_url)
locations_doc = lxml.html.fromstring(locations_response.content)

for location in locations_doc.cssselect("ul[data-role=listview] li:not([data-role=list-divider]) a"):
	location_name = location.text
	location_id = location.get('id')

	print location_name, location_id

	washers_dryers_url = "http://m.laundryview.com/submitFunctions.php?monitor=true&lr=%s&cell=null" % location.get('id')
	washers_dryers_response = requests.get(washers_dryers_url)
	washers_dryers_doc = lxml.html.fromstring(washers_dryers_response.content)

	washer = washers_dryers_doc.cssselect("#washer")[0]
	while True:
		washer = washer.getnext()
		if washer is None or washer.get('id') != None: break
		washer_index = [x for x in washer.itertext()][0].strip()
		washer_status = washer.cssselect('a:nth-child(1)')[0].getchildren()[2].text
		washer_id = washer.cssselect('a')[0].get('id')
		print "\t", "washer", washer_id, washer_index, washer_status

	dryer = washers_dryers_doc.cssselect("#dryer")[0]
	while True:
		dryer = dryer.getnext()
		if dryer is None or dryer.get('id') != None: break
		dryer_index = [x for x in dryer.itertext()][0].strip()
		dryer_status = dryer.cssselect('a:nth-child(1)')[0].getchildren()[2].text
		dryer_id = dryer.cssselect('a')[0].get('id')
		print "\t", "dryer", dryer_id, dryer_index, dryer_status
