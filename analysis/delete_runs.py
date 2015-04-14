from firebase import firebase
firebase = firebase.FirebaseApplication('https://aljohri-nulaundry.firebaseio.com', None)
machines = firebase.get("/machines", None)

for machine_id, machine in machines.iteritems():
	print "Deleting %s" % machine_id
	firebase.delete(url='/machines/%s' % machine_id, name="runs")