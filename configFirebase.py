import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://reconnaissance-faciale-e632a-default-rtdb.firebaseio.com/'
})

ref = db.reference("Employes")

data = {
    "8080": {
        "prenom": "Abdoulaziz",
        "nom": "Maïga",
        "email": "maigabdoul@ewaati.com",
        "numero": "79522067",
        "dernier_pointage": "2023-11-21 12:02:34",
        "total_pointage": 9
    },
    "2222": {
        "prenom": "Sidy",
        "nom": "Keïta",
        "email": "sidik@ewaati.com",
        "numero": "75330990",
        "dernier_pointage": "2023-11-21 12:04:34",
        "total_pointage": 4
    },
    "3232": {
        "prenom": "Karim",
        "nom": "Diawara",
        "email": "kdiawara@ewaati.com",
        "numero": "72332454",
        "dernier_pointage": "2023-11-21 12:10:34",
        "total_pointage": 6
    },
    "4444": {
        "prenom": "Lamba",
        "nom": "Traoré",
        "email": "lbtraore@ewaati.com",
        "numero": "89090900",
        "dernier_pointage": "2023-11-21 12:14:34",
        "total_pointage": 10
    },
    "9696": {
        "prenom": "Elon",
        "nom": "Musk",
        "email": "elmusk@ewaati.com",
        "numero": "33783378",
        "dernier_pointage": "2023-11-21 12:11:34",
        "total_pointage": 8
    }
}

for key, value in data.items():
    ref.child(key).set(value)


