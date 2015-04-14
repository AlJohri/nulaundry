from firebase import firebase
firebase = firebase.FirebaseApplication('https://aljohri-nulaundry.firebaseio.com', None)
from pprint import pprint as pp

machines = firebase.get("/machines", None)

machine = machines['33057']
statuses = machine.pop('statuses')

pp(machine)

statuses = sorted(statuses.values(), key=lambda x: x[0])

for status in statuses:
	print status