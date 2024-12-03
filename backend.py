import sys
from aggregator.FireBase import FirebaseService
from aggregator.data_pipe import DataPipe
from aggregator.sentiment_analysis import Aggregator
from aggregator.sentiment_analysis import Crawler


default_model="finiteautomata/bertweet-base-sentiment-analysis"

def main():

    #
    # Totally dumb and synchronous for now. Just create the pipe and put hard-coded data on it. Then
    # read the data from the queue, perform sentiment analysis and write the output to the database.
    #
    crawler_pipe = DataPipe( "CrawlerPipe" )
    ds = Crawler( "Crawler", crawler_pipe.output_pipe )
    firebase = FirebaseService( "FirebaseService" )
    agg = Aggregator( "Aggregator", crawler_pipe.input_pipe, firebase, default_model )
    #firebase.get_crypto_data( "Bitcoin/7" )
    #firebase.put_crypto_data()
    
    ds.run()
    agg.run()
    
if __name__ == '__main__':
    sys.exit(main())
