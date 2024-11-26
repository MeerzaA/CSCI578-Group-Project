from transformers import pipeline
import sys
from time import sleep

# Placeholder class to simulate a data stream
class DataPipe:

    # The end of the pipe to which a component writes its output data
    class OutputDataPipe:

        def write( self, item ):
           self.queue.append( item ) 

        def __init__( self, queue ):
            self.queue = queue
            
    # The end of the pipe from which a compenent gets its input data
    class InputDataPipe:

        def read( self ):
           
            if len( self.queue ) > 0:
                item = self.queue[0]
                self.queue.pop(0)
                return item
            
            return None

        def __init__( self, queue ):
            self.queue = queue


    def __init__( self, name ):
        print( f"{name} initializing" )
        self.name = name
        self.queue = []
        self.output_pipe = self.OutputDataPipe( self.queue )
        self.input_pipe = self.InputDataPipe( self.queue )
        print( f"{name} initialized" )

# Placeholder class for web crawler
class Crawler:

    def send( self, item ):
        self.out_pipe.write( item )
        
    # Just send all the hard-coded data to the output pipe
    def run( self ):
        for item in self.data:
            self.send( item )
        print( f"{self.name} exiting")

    def __init__( self, name, out_pipe ):
        print( f"{name} initializing" )
        self.name = name
        # Combination  of positive, negative, and neutral data. Some are attempts to fool the model. "Bitcoin is the shit" fools the current default model.
        self.data = [["I love bitcoin.", "Bitcoin blows"], ["Bitcoin is the absolute best at being the worst possible thing."], ["Bitcoin is the shit.", "How do I buy Bitcoin?"] ]
        self.out_pipe = out_pipe
        print( f"{name} initialized" )
        

default_model="finiteautomata/bertweet-base-sentiment-analysis"
class Aggregator:

    def analyzeSentiment( self, input_data ):
        print( input_data )
        return self.sentiment_pipeline( input_data )

    # Placeholder method for writing sentiment data to Firebase
    def writeToDatabase( self, output_data ):
        print( output_data )

    # Continue trying to read data from the pipe until Ctrl-C is pressed
    def run(self):

        try:
            while True:
                input_data = self.in_pipe.read()  
                if input_data is not None:
                    sentiment_data = self.analyzeSentiment( input_data )
                    for output_item in sentiment_data:
                        self.writeToDatabase( output_item )
                else:
                    print( "Waiting for data" )
                    # Not the best practice, but sleep for one second before trying to read more data.
                    sleep(1.0)

        except KeyboardInterrupt:
            pass
        

    def __init__( self, name, in_pipe, model_to_use=default_model):
        print( f"{name} initializing" )
        self.name = name
        self.sentiment_pipeline = pipeline( model=model_to_use )
        self.in_pipe = in_pipe
        print( f"{name} initialized" )

def main():

    #
    # Totally dumb and synchronous for now. Just create the pipe and put hard-coded data on it. Then
    # read the data from the queue, perform sentiment analysis and write the output to the database.
    #
    pipe = DataPipe( "Pipe" )
    ds = Crawler( "Crawler", pipe.output_pipe )
    agg = Aggregator( "Aggregator", pipe.input_pipe, default_model )
    
    ds.run()
    agg.run()
    firebase = FirebaseService()
    firebase.get_crypto_data()
    
if __name__ == '__main__':
    sys.exit(main())