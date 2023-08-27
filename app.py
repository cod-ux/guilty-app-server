#Write code to intialize firebase from credentials.json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

users_ref = db.collection('users')

#write code to get list of all docs from firestore
docs = users_ref.stream()

# write code to read data from a particular doc
doc_ref = db.collection('users').document('42xGhEiG9Fe0YZ2DAOBoFHTDEYF2')

print(doc_ref.get().to_dict())