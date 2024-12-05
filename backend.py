import sys

from aggregator.FireBase import FirebaseService
from aggregator.data_pipe import DataPipe
from aggregator.sentiment_analysis import Aggregator
from aggregator.sentiment_analysis import Crawler


#default_model="finiteautomata/bertweet-base-sentiment-analysis"
#default_model="cardiffnlp/twitter-roberta-base-sentiment" # labels things neutral too much
#default_model="cardiffnlp/twitter-roberta-large-topic-sentiment-latest" # labels things neutral too much
#default_model="siebert/sentiment-roberta-large-english" #Correctly classifies tricky cases, but fails neutral.
#default_model="distilbert/distilbert-base-uncased-finetuned-sst-2-english" wrong a lot

def main():    
    crawler_pipe = DataPipe( "CrawlerPipe" )
    ds = Crawler( "Crawler", crawler_pipe.output_pipe )
    firebase = FirebaseService( "FirebaseService" )
    agg = Aggregator("Aggregator", in_pipe=crawler_pipe.input_pipe, firebase_service=firebase)
    
    ds.run()
    agg.run()
    
if __name__ == '__main__':
    sys.exit(main())
