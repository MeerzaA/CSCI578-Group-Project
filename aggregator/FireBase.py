import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db  # Use this for Realtime Database


class FirebaseService:



    def __init__(self):
        self.connection = self.connect_to_firebase()
        self.crypto_counter = {}

    def connect_to_firebase(self):
        # Firebase initialization logic
        load_dotenv()
        sdk_cert_path = os.getenv("ADMIN_SDK_CERT_PATH")
        if not sdk_cert_path:
            raise ValueError("Environment variable ADMIN_SDK_CERT_PATH is not set or accessible.")
        cred = credentials.Certificate(sdk_cert_path)
        firebase_admin.initialize_app(cred, {"databaseURL": "https://crypto-board-csci578-default-rtdb.firebaseio.com/"})
        pass

    def get_crypto_data(self, crypto_name):
        # Logic to fetch data from Firebase

        # Reference a specific path in the database
        counter = self.crypto_counter[crypto_name]
        ref = db.reference(f"{crypto_name}/{counter}")

        # Get data at this path
        data = ref.get()

        print(data)
        pass

    # mostly used chatgpt for this function
    def put_crypto_data(self,crypto_name, data):

        # Increment counter for the given crypto name
        if crypto_name not in self.crypto_counter:
            self.crypto_counter[crypto_name] = 0
        self.crypto_counter[crypto_name] += 1

        # Use the counter as part of the key
        counter = self.crypto_counter[crypto_name]

        # Comes up with crypto path + sends data
        ref = db.reference(f"{crypto_name}/{counter}")
        ref.set(data)

        print("New data has been added to the database.")
        pass





