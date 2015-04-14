from firebase import firebase
firebase = firebase.FirebaseApplication('https://aljohri-nulaundry.firebaseio.com', None)
machines = firebase.get("/machines", None)

for machine_id, machine in machines.iteritems():
	num_runs = len(machine['runs'].values()) if machine.get('runs') else 0
	print "Machine %s has %d runs" % (machine_id, num_runs)
	firebase.put(url='/machines/%s' % machine_id, name="runs", data=num_runs)