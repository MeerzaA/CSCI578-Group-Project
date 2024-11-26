import firebase_admin
from firebase_admin import credentials
from firebase_admin import db  # Use this for Realtime Database

class FirebaseService:
    def __init__(self):
        self.connection = self.connect_to_firebase()
        print("kevin kuo - test 123")

    def connect_to_firebase(self):
        # Firebase initialization logic
        cred = credentials.Certificate('/Users/bbpk/PycharmProjects/pythonProject5/crypto-board-csci578-firebase-adminsdk-srcrn-c7680a0a8d.json')
        firebase_admin.initialize_app(cred, {"databaseURL": "https://crypto-board-csci578-default-rtdb.firebaseio.com/"})
        pass

    def get_crypto_data(self):
        # Logic to fetch data from Firebase

        # Reference a specific path in the database
        ref = db.reference("Bitcoin/0/Source")

        # Get data at this path
        data = ref.get()

        print(data)
        pass

    #need to add parameters CRYPTO_TYPE, actual data,
    def put_crypto_data(self):
        # Logic to fetch data from Firebase

        #this number works. need to figure out counter per coin. replace 7 with counter var
        ref = db.reference("Bitcoin/7")

        # Add a new entry without overwriting
        new_data = {
            "Sentiment": "420.0",
            "Site": "twitter",
            "Source": "Social Medial",
            "date": "1993-05-02",
            "link": "www.twitter.com"
        }
        ref.push(new_data)

        print("New data has been added to the database.")
        pass





