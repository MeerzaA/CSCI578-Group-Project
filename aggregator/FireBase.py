import firebase_admin
from firebase_admin import credentials, db
import os
import logging

class FirebaseService:
    def __init__(self, name):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.connection = self.connect_to_firebase()
        self.name = name
        self.counts = { 
            'Bitcoin': {}, 
            'Ethereum': {}, 
            'Solana': {}, 
            'Ripple': {}, 
            'Litecoin': {}, 
            'Dogecoin': {}, 
            'BNB': {}, 
            'Cardano': {}, 
            'Avalanche': {}, 
            'Shiba Inu': {}} 

        for key in self.counts:
            ref = db.reference(key)
            dates = ref.get()
            if dates:
                for date, data in dates.items():
                    self.counts[key][date] = len(data)
            else:
                self.counts[key] = {}
    
        self.logger.info(f"Current DB counts: {self.counts}")
        self.logger.info(f"{name} initialized.")
    
    def connect_to_firebase(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        cred_path = os.path.join(current_dir, 'crypto-board-csci578-firebase-adminsdk-srcrn-e7c778da94.json')
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {"databaseURL": "https://crypto-board-csci578-default-rtdb.firebaseio.com/"})
        self.logger.info("Connected to Firebase.")
    
    def put_crypto_data(self, output_data):
        try:
            currency = output_data['currency']
            date = output_data['date']
            del output_data['currency']
            del output_data['date']

            # Initialize counts for currency and date if not present
            if date not in self.counts[currency]:
                self.counts[currency][date] = 0

            # Increment count
            self.counts[currency][date] += 1
            count = self.counts[currency][date]

            # Define Firebase path as 'currency/date/count'
            tag = f"{currency}/{date}/{count}"

            ref = db.reference(tag)
            ref.set(output_data)  
            self.logger.info(f"New data added to Firebase under {tag}: {output_data}")
        except Exception as e:
            self.logger.error(f"Failed to write data to Firebase: {e}") 


