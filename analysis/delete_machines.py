from firebase import firebase
firebase = firebase.FirebaseApplication('https://aljohri-nulaundry.firebaseio.com', None)
firebase.delete(url='/machines', name=None)