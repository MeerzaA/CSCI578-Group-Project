from transformers import pipeline
from time import sleep
import json
import stanza
import re
from threading import Thread
from aggregator.reddit_crawler import RedditCrawler

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraper_Files.CryptoBoard_Scraper.spiders.BlockworkSpider import BlockworkSpider
import os

# Placeholder class for web crawler
class Crawler:
       
    def __init__( self, name, out_pipe ):
        self.out_pipe = out_pipe
        self.name = name

    def send( self, item ):
        """Send an item to the output pipe."""
        self.out_pipe.write( item )
        
    def run( self ):
        # Run the Reddit crawling process.
        #self._redditCrawlThread = Thread(target=self._start_reddit_crawler)
        #self._redditCrawlThread.start()

        # TODO: Run the scrap crawling procses
        print("yay.")
        settings_file_path = 'scraper_Files.CryptoBoard_Scraper.settings' # The path seen from root, ie. from main.py
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        process = CrawlerProcess( get_project_settings() )
        process.crawl( BlockworkSpider, out_pipe=self.out_pipe )
        process.start()
        print("double yay.")

    def _start_reddit_crawler(self):
        """Internal method to run the Reddit crawler in the background."""
        print("Reddit crawling started.")
        reddit_crawler = RedditCrawler()
        reddit_crawler.crawl(self.send)
        print("Reddit crawling completed.")
        
#TODO: move to config file
default_sentiment_model = "cardiffnlp/twitter-roberta-large-topic-sentiment-latest" 
default_summarizer_model = "google/pegasus-x-large"
key_map = {
        'Bitcoin': 'Bitcoin',
        'BTC': 'Bitcoin',
        '@BTC': 'Bitcoin',
        'Ethereum': 'Ethereum',
        'ETH': 'Ethereum',
        '@ETH': 'Ethereum',
        'Solana': 'Solana',
        'SOL': 'Solana',
        '@SOL': 'Solana',
        'Ripple': 'Ripple',
        'XRP': 'Ripple',
        '@XRP': 'Ripple',
        'Litecoin': 'Litecoin',
        'LTC': 'Litecoin',
        '@LTC': 'Litecoin',
        'Dogecoin': 'Dogecoin',
        'DOGE': 'Dogecoin',
        '@DOGE': 'Dogecoin',
        'Binance Coin': 'Binance Coin',
        'BNB': 'BNB',
        '@BNB': 'BNB',
        'Cardano': 'Cardano',
        'ADA': 'Cardano',
        '@ADA': 'Cardano',
        'Avalanche': 'Avalanche',
        'AVAX': 'Avalanche',
        '@AVAX': 'Avalanche',
        'Shiba Inu': 'Shiba Inu',
        'SHIB': 'Shiba Inu',
        '@SHIB': 'Shiba Inu'
    }

def init_list_dict( keys ):
    return { key_map[key]: [] for key in keys }

def init_dict( keys ):
    return { key_map[key]: None for key in keys }

class TextSummarizer:
    
    def __init__(self, model_name=default_summarizer_model):
        
        self.summarizer_pipeline = pipeline( 'summarization', model=model_name )
        
    def summarize_text( self, text_to_summarize ):
        return self.summarizer_pipeline( text_to_summarize )


class SentimentAnalyzer:
    
    def __init__(self, sentiment_model=default_sentiment_model, summarizer_model=default_summarizer_model, name="SentimentAnalyzer"):
        self.name = name
        self.sentiment_pipeline = pipeline( 'text-classification', model=sentiment_model )
        self.text_summarizer = TextSummarizer( summarizer_model )
        stanza.download('en')
        self.snlp = stanza.Pipeline('en')

    def shouldSummarize( self, input_text ):
        if len( input_text ) > 512:
            print( f"Producing summary because text length is {len(input_text)}")
            return True
        
        return False
       
    def windowedSentenceSentiment( self, topic_list, input_text, window_size=2 ):
        doc = self.snlp( input_text )
        num_sentences = len( doc.sentences )
        if window_size > num_sentences:
            return None

        sentiments = init_list_dict( topic_list )
        for window_idx in range( num_sentences - window_size ):
            sentence_window = ""
            for sentence_idx in range( window_idx, window_idx+window_size ):
                sentence_window += doc.sentences[sentence_idx].text
            
            for topic in topic_list:
                text_to_analyze = self.create_query( topic, sentence_window )
                sentiments[key_map[topic]].append( self.sentiment_pipeline( text_to_analyze ) )
        
        return sentiments

    def generateSentimentValue( self, sentiment_output ):
        label_map = { 'strongly negative': 2, 'negative': 4, 'negative or neutral': 6, 'positive': 8, 'strongly positive': 10 } 
        label = sentiment_output['label']
        score = sentiment_output['score']

        return label_map[label] + 2*score
        
    def analyzeSentiment( self, topic_list, title, input_text ):

        if self.shouldSummarize( input_text ):
            summaries = self.text_summarizer.summarize_text( input_text )
            input_text = summaries[0]['summary_text']

        found_topics = self.find_topics_strings( input_text )

        sentiments = init_dict( found_topics )
        for topic in found_topics: 
            text_to_analyze = self.create_query( topic, input_text )
            sentiment_output = self.sentiment_pipeline( text_to_analyze )
            sentiments[key_map[topic]] = self.generateSentimentValue( sentiment_output[0] )
        #print( sentiments ) 
        return sentiments 


    def find_topics_strings( self, text ):

        found_topics = []
        for topic in key_map:

            if topic.find('@') > 0 :
                continue

            pattern = r'\b' + topic.lower() + r'\b'
            #print(pattern)
            #print(text)
            if re.search( pattern, text ) is not None:
                found_topics.append( topic )

        return found_topics
    
    def create_query( self, topic, text ):
        return f"{text} </s> {topic}"
         
        
class Aggregator:
    
    # Placeholder method for writing sentiment data to Firebase
    def writeToDatabase( self, output_item ):
        self.firebase_service.put_crypto_data( output_item )

    def parseJsonElement( self, input_data ):
        source = input_data.get('source_name', 'Unknown')
        source_type = input_data.get('source_type', 'Unknown')
        date = input_data.get('date', 'Unknown')
        currencies = input_data.get('cryptocurrency', 'Unknown' )
        title = input_data.get('title', 'Unknown')
        url = input_data.get('url', 'Unknown' )
        text = input_data.get('text','Unknown')

        return source, source_type, date, currencies, title, url, text

    def preprocessText( self, text ):
        return text.lower()

    def processInput( self, input_data ):
        
        for input_item in input_data.values():
            source, source_type, date, currencies, title, url, text = self.parseJsonElement( input_item[0] ) #Things coming from the BlockworkSpider are single-element lists

            text = self.preprocessText( text )
            print(text)
            sentiments = self.sentiment_analyzer.analyzeSentiment( currencies, title, text )
            print( "Sentiments: ", sentiments )
            if sentiments is not None:
                for currency, sentiment in sentiments.items():
                    output_item = {'currency':currency, 'source_name': source, 'source_type': source_type, 'date':date, 'title':title, 'url':url, 'sentiment': sentiment }
                    self.writeToDatabase( output_item )

    # Continue trying to read data from the pipe until Ctrl-C is pressed
    def run( self ):
        try:
            while True:
                input_data = self.in_pipe.read()  
                if input_data is not None:
                    print("GOT A THING!")
                    self.processInput( input_data )
                else:
                    print( "Waiting for data" )
                    # Not the best practice, but sleep for one second before trying to read more data.
                    sleep(1.0)

        except KeyboardInterrupt:
            pass
        

    def __init__( self, name, in_pipe, firebase_service ):
        print( f"{name} initializing" )
        self.name = name
        self.in_pipe = in_pipe
        self.sentiment_analyzer = SentimentAnalyzer()
        self.firebase_service = firebase_service
        print( f"{name} initialized" )
