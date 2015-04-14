from firebase import firebase
firebase = firebase.FirebaseApplication('https://aljohri-nulaundry.firebaseio.com', None)
machines = firebase.get("/machines", None)

import itertools
from collections import defaultdict

def normal_date(timestamp):
	return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

for machine_id, machine in machines.iteritems():

	# if machine_id != '33057': continue

	statuses = sorted(machine['statuses'].values(), key=lambda x: x[0])

	for timestamp, status in reversed(statuses):
		if status == "Avail":

			all_avails = [tm for tm,st in statuses[:-1] if st == "Avail" and tm < timestamp]
			last_avail_timestamp = all_avails[-1] if all_avails else None
			last_avail_timestamp_index = statuses.index([last_avail_timestamp, "Avail"]) if last_avail_timestamp else None
			timestamp_after_last_avail = statuses[last_avail_timestamp_index + 1][0] if last_avail_timestamp_index else None

			if timestamp_after_last_avail:
				firebase.post(url='/machines/%s/runs' % machine_id, data=(timestamp_after_last_avail, timestamp), headers={'print': 'pretty'})
				print machine_id, "Run Complete:", timestamp_after_last_avail, timestamp

# statuses_list = sorted(statuses.values(), key=lambda x : (x['id'], x['timestamp']) )

# for machine_id, machine_statuses in itertools.groupby(statuses_list, lambda item: item["id"]):
# 	print machine_id
# 	previous_status = ""

# 	machine_run_number = 0
# 	machine_runs = defaultdict(list)

# 	for status in machine_statuses:
# 		if status['status'] == 'Avail':
# 			machine_run_number += 1
# 		# print "\t", status['timestamp'], status['type'], status['status']
# 		machine_runs[machine_run_number].append(status)

# 	for run_number, runs in machine_runs.iteritems():
# 		print run_number
# 		for run in runs:
# 			print "\t", run
