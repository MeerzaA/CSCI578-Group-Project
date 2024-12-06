import firebase_admin
from firebase_admin import credentials, db
import os
import logging

empty_element = {'Unknown': 0}
class FirebaseService:
    def __init__(self, name):
        self.logger = logging.getLogger(self.__class__.__name__)
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
        cred_path = os.path.join(current_dir,'crypto-board-csci578-firebase-adminsdk-srcrn-e7c778da94.json')
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {"databaseURL": "https://crypto-board-csci578-default-rtdb.firebaseio.com/"})
        self.logger.info("Connected to Firebase.")
    

    def put_crypto_data(self, output_data):
        try:
            # we need to look for the required keys and not push if anything is missing
            required_keys = ['currency', 'date', 'sentiment', 'source_name', 'source_type', 'title', 'url']
            for key in required_keys:
                if key not in output_data:
                    self.logger.error(f"Missing required key: {key} in output data. Skipping push to Firebase.")
                    return  

            # check for values that say 'Unknown'
            if output_data['currency'] == 'Unknown' or output_data['date'] == 'Unknown':
                self.logger.error("Invalid data: currency or date is 'Unknown'. Skipping push to Firebase.")
                return

            for key in ['sentiment', 'source_name', 'source_type', 'title', 'url']:
                if output_data.get(key) == 'Unknown':
                    self.logger.error(f"Invalid data: {key} is 'Unknown'. Skipping push to Firebase.")
                    return

            # Process and push data to Firebase
            currency = output_data['currency']
            date = output_data['date']
            del output_data['currency']
            del output_data['date']

            current_count = self.counts[currency].get(date, 0)

            tag = currency + f"/{date}/{current_count+1}"
            ref = db.reference(tag)
            ref.update(output_data)

            self.counts[currency][date] = current_count + 1

            print("New data has been added to the database.")

            # Set the final count and store the data
            count = self.counts[currency][date]
            tag = f"{currency}/{date}/{count}"
            ref = db.reference(tag)
            ref.set(output_data)

            self.logger.info(f"New data added to Firebase under {tag}: {output_data}")

        except Exception as e:
            self.logger.error(f"Failed to write data to Firebase: {e}")


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
            
            ref = db.reference(tag)
            
            ref.update(output_data)

            self.counts[currency][date] = current_count + 1
            
            print("New data has been added to the database.")
            
            count = self.counts[currency][date]
            tag = f"{currency}/{date}/{count}"

            ref = db.reference(tag)
            ref.set(output_data)
            
            self.logger.info(f"New data added to Firebase under {tag}: {output_data}")
        
