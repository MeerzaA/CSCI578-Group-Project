import firebase_admin
from firebase_admin import credentials
from firebase_admin import db  # Use this for Realime Database

import os

empty_element = {'Unknown': 0}
class FirebaseService:
    def __init__(self, name ):
        self.connection = self.connect_to_firebase()
        self.name = name

        self.counts = { 'Bitcoin': empty_element,
                        'Ethereum': empty_element,
                        'Solana': empty_element,
                        'Ripple': empty_element,
                        'Litecoin': empty_element,
                        'Dogecoin': empty_element,
                        'Binance Coin': empty_element,
                        'Cardano': empty_element,
                        'Avalanche': empty_element,
                        'Shiba Inu': empty_element,
        }

        for key in self.counts:
            date, count = self.get_count_for_tag( key )
            if date is not None:
                self.counts[key][date] = count
            else:
                self.counts[key]['Unknown'] += count
        

        print( 'current db counts-- ', self.counts )
        print( f"{name} initialized.")
        

    def connect_to_firebase( self ):
   
        current_dir = os.path.dirname(os.path.abspath(__file__))
        cred_path = os.path.join(current_dir, 'crypto-board-csci578-firebase-adminsdk-srcrn-c7680a0a8d.json')
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {"databaseURL": "https://crypto-board-csci578-default-rtdb.firebaseio.com/"})

    def get_crypto_data(self):
        # Logic to fetch data from Firebase

        # Reference a specific path in the database
        ref = db.reference("Bitcoin/0/Source")

        # Get data at this path
        data = ref.get()

        print(data)

    def get_count_for_tag( self, tag ):
        ref = db.reference( tag ) 
        dates = ref.get()
        if dates is not None:
            for date, data in dates.items():
                return date, len(data)
        else:
            return None, 0
        
    def put_crypto_data(self, output_data):
        currency = output_data['currency']
        date = output_data['date']
        del output_data['currency'] 
        del output_data['date']
        current_count = self.counts[currency].get(date, 0)
        tag = currency + f"/{date}/{current_count+1}"
        ref = db.reference( tag )
        ref.update( output_data )
        self.counts[currency][date] = current_count + 1
        
        print("New data has been added to the database.")




