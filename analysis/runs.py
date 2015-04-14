from firebase import firebase
firebase = firebase.FirebaseApplication('https://aljohri-nulaundry.firebaseio.com', None)
statuses = firebase.get("/status", None)

import itertools

statuses_list = sorted(statuses.values(), key=lambda x : (x['id'], x['timestamp']) )

for machine_id, machine_statuses in itertools.groupby(statuses_list, lambda item: item["id"]):
	print machine_id
	for status in machine_statuses:
		print "\t", status['timestamp'], status['type'], status['status']