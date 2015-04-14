from firebase import firebase
firebase = firebase.FirebaseApplication('https://aljohri-nulaundry.firebaseio.com', None)
statuses = firebase.get("/status", None)

import itertools
from collections import defaultdict

statuses_list = sorted(statuses.values(), key=lambda x : (x['id'], x['timestamp']) )

for machine_id, machine_statuses in itertools.groupby(statuses_list, lambda item: item["id"]):
	print machine_id
	previous_status = ""

	machine_run_number = 0
	machine_runs = defaultdict(list)

	for status in machine_statuses:
		if status['status'] == 'Avail':
			machine_run_number += 1
		# print "\t", status['timestamp'], status['type'], status['status']
		machine_runs[machine_run_number].append(status)

	for run_number, runs in machine_runs.iteritems():
		print run_number
		for run in runs:
			print "\t", run
