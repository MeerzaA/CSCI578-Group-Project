import firebase_admin
from firebase_admin import credentials
from firebase_admin import db  # Use this for Realime Database

class FirebaseService:
    def __init__(self, name ):
        self.connection = self.connect_to_firebase()
        self.name = name
        self.counts = { 'Bitcoin': -1, 'Ethereum': 0 } # For some reason Bitcoin has a phantom element that is being returned. Accounting for it here until it can be properly corrected.

        for key in self.counts:
            self.counts[key] += self.get_count_for_tag( key )
        
        print( 'current db counts-- ', self.counts )
        print( f"{name} initialized.")
        

    def connect_to_firebase( self ):
        # Firebase initialization logic
        cred = credentials.Certificate('aggregator/crypto-board-csci578-firebase-adminsdk-srcrn-c7680a0a8d.json')
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
        data = ref.get()
        return len(data)
        
    def put_crypto_data( self, output_data ):
        
        currency = output_data['currency']
        del output_data['currency'] 
        current_count = self.counts[currency] 
        tag = currency + f"/{current_count+1}"
        ref = db.reference( tag )
        ref.update( output_data )
        self.counts[currency] += 1
        
        print("New data has been added to the database.")





