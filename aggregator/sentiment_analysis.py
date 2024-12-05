from transformers import pipeline, AutoTokenizer
from time import sleep
import json
import stanza
import re
from threading import Thread
from .reddit_crawler import RedditCrawler
import logging

#scrapy 
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from scrapy.signalmanager import dispatcher
# Spiders
from scraper_Files.CryptoBoard_Scraper.spiders.BlockworkSpider import BlockworkSpider
from scraper_Files.CryptoBoard_Scraper.spiders.DecryptSpider import DecryptSpider

# Placeholder class for web crawler
class Crawler:
       
    def __init__( self, name, out_pipe ):
        self.out_pipe = out_pipe
        self.name = name
        self.crawler_process = CrawlerProcess(get_project_settings()) 
        self.crawler_process.crawl(BlockworkSpider)  
        self.crawler_process.crawl(DecryptSpider)

    def send( self, item ):
        """Send an item to the output pipe."""
        self.out_pipe.write( item )
        
    def run( self ):
        # Start Scrapy crawl process 
        self._scrapy_thread = Thread(target=self._start_scrapy_crawl)
        self._scrapy_thread.start()
        
        # Run the Reddit crawling process.
        self._redditCrawlThread = Thread(target=self._start_reddit_crawler)
        self._redditCrawlThread.start()

        # TODO: Run the scrap crawling procses
        
    def _start_scrapy_crawl(self):
        """Internal method to run the Scrapy crawler in the background."""
        print("Scrapy crawling started.")
        self.crawler_process.start()  # Starts both crawlers
        print("Scrapy crawling completed.")
        
    def _start_reddit_crawler(self):
        """Internal method to run the Reddit crawler in the background."""
        print("Reddit crawling started.")
        reddit_crawler = RedditCrawler()
        reddit_crawler.crawl(self.send)
        print("Reddit crawling completed.")
        
#TODO: move to config file
default_sentiment_model = "cardiffnlp/twitter-roberta-large-topic-sentiment-latest" 
#default_summarizer_model = "human-centered-summarization/financial-summarization-pegasus"#facebook/bart-large-cnn"
default_summarizer_model = "google/pegasus-x-large"#"human-centered-summarization/financial-summarization-pegasus"
from transformers import AutoTokenizer, PegasusXModel,PegasusTokenizer, PegasusXForConditionalGeneration

key_map = { 
    # Bitcoin
    'BTC': 'Bitcoin', '@BTC': 'Bitcoin', 'Bitcoin': 'Bitcoin',
    # Ethereum
    'ETH': 'Ethereum', '@ETH': 'Ethereum', 'Ethereum': 'Ethereum',
    # Solana
    'SOL': 'Solana', '@SOL': 'Solana', 'Solana': 'Solana',
    # Ripple
    'Ripple': 'Ripple', 'XRP': 'Ripple', '@XRP': 'Ripple',
    # Litecoin
    'Litecoin': 'Litecoin', 'LTC': 'Litecoin', '@LTC': 'Litecoin',
    # Dogecoin
    'Dogecoin': 'Dogecoin', 'DOGE': 'Dogecoin', '@DOGE': 'Dogecoin',
    # Binance Coin
    'BNB': 'BNB', '@BNB': 'BNB',
    # Cardano
    'Cardano': 'Cardano', 'ADA': 'Cardano', '@ADA': 'Cardano',
    # Avalanche
    'Avalanche': 'Avalanche', 'AVAX': 'Avalanche', '@AVAX': 'Avalanche',
    # Shiba Inu
    'Shiba Inu': 'Shiba Inu', 'SHIB': 'Shiba Inu', '@SHIB': 'Shiba Inu',
}

def init_list_dict( keys ):
    return { key_map[key]: [] for key in keys }

def init_dict( keys ):
    return { key_map[key]: None for key in keys }

class TextSummarizer:
    
    def __init__(self, model_name=default_summarizer_model):
        self.summarizer_pipeline = pipeline('summarization', model=model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    def summarize_text(self, text_to_summarize, topics, max_length=406, min_length=100):
        # Prepend topics to ensure they are retained in the summary
        combined_text = f"Topics: {', '.join(topics)}. " + text_to_summarize
        
        # Truncate the combined text if it's too long for the model
        inputs = self.tokenizer.encode(combined_text, return_tensors='pt', truncation=True, max_length=1024)
        truncated_text = self.tokenizer.decode(inputs[0], skip_special_tokens=True)
        
        # Perform summarization
        summary = self.summarizer_pipeline(truncated_text, max_length=max_length, min_length=min_length, truncation=True)
        return summary



class SentimentAnalyzer:
    
    def __init__(self, sentiment_model=default_sentiment_model, summarizer_model=default_summarizer_model, name="SentimentAnalyzer"):
        self.name = name
        self.sentiment_pipeline = pipeline('text-classification', model=sentiment_model)
        self.text_summarizer = TextSummarizer(summarizer_model)
        stanza.download('en')
        self.snlp = stanza.Pipeline('en')
        self.tokenizer = AutoTokenizer.from_pretrained(summarizer_model)  # Add tokenizer for summarization
    
    def shouldSummarize(self, input_text):
        print("---- SHOULD SUMMARIZE FUNC ----")
        max_length = 512  # Define based on model's maximum token limit
        if len(input_text) > max_length:
            print(f"Producing summary because text length is {len(input_text)}")
            return True
        return False
    
    def windowedSentenceSentiment(self, topic_list, input_text, window_size=2):
        print("----  windowedSentenceSentiment FUNC ----")
        doc = self.snlp(input_text)
        num_sentences = len(doc.sentences)
        if window_size > num_sentences:
            return None

        sentiments = init_list_dict(topic_list)
        for window_idx in range(num_sentences - window_size + 1):
            sentence_window = " ".join([doc.sentences[sentence_idx].text for sentence_idx in range(window_idx, window_idx+window_size)])
            
            for topic in topic_list:
                text_to_analyze = self.create_query(topic, sentence_window)
                sentiments[key_map[topic]].append(self.sentiment_pipeline(text_to_analyze))
        
        return sentiments
    
    def generateSentimentValue(self, sentiment_output):
        print("---- generateSentimentValue FUNC ----")
        print(f"Sentiment output: {sentiment_output}")  # Add this line to debug sentiment output
        label_map = { 'strongly negative': 2, 'negative': 4, 'negative or neutral': 6, 'positive': 8, 'strongly positive': 10 } 
        label = sentiment_output['label']
        score = sentiment_output['score']

        return label_map.get(label, 0) + 2 * score  # Use get to avoid KeyError
    
    def analyzeSentiment(self, topic_list, title, input_text):
        print("---- analyzeSentiment FUNC ----")
        print(f"Input text length: {len(input_text)}")

        # Extract topics from the original input text
        found_topics = self.find_topics_strings(input_text)
        print(f"Found topics: {found_topics}")  # Debugging line to confirm found topics

        if not found_topics:
            print("No topics found. Skipping sentiment analysis.")
            return {}

        if self.shouldSummarize(input_text):
            summarized_text = self.text_summarizer.summarize_text(input_text, found_topics)
            if summarized_text and len(summarized_text) > 0:
                print("Text has been summarized.")
                input_text = summarized_text[0]['summary_text']
            else:
                print("Summarization failed. Proceeding with original text.")

        sentiments = init_dict(found_topics)
        for topic in found_topics:
            text_to_analyze = self.create_query(topic, input_text)
            print(f"Text to analyze for {topic}: {text_to_analyze}")  # Debugging line to confirm text being analyzed
            sentiment_output = self.sentiment_pipeline(text_to_analyze)
            print(f"Sentiment output for {topic}: {sentiment_output}")  # Debugging line to confirm sentiment output

            if sentiment_output:
                sentiments[key_map[topic]] = self.generateSentimentValue(sentiment_output[0])
            else:
                print(f"Sentiment analysis failed for {topic}")

        print(f"Sentiment analysis result: {sentiments}")
        return sentiments

    def find_topics_strings(self, text):
        print("---- find_topics_strings FUNC ----")
        
        target_topics = [
            'BTC', 'ETH', 'SOL', 'XRP', 'LTC', 'DOGE', 'ADA', 'AVAX', 'SHIB',
            'Bitcoin', 'Ethereum', 'Solana', 'Ripple', 'Litecoin', 'Dogecoin', 'BNB', 'Cardano', 'Avalanche', 'Shiba Inu'
            ]

        found_topics = []
        text_lower = text.lower()
        for topic in target_topics:
            pattern = r'\b' + re.escape(topic.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_topics.append(topic)

        return found_topics
    
    def create_query(self, topic, text):
        print("---- create_query FUNC ----")
        return f"{text} </s> {topic}"
            
class Aggregator:
    
    # Placeholder method for writing sentiment data to Firebase
    def writeToDatabase(self, output_item):
        print(f"Writing to Firebase: {output_item}")  # Debugging line to confirm it's being reached
        try:
            self.firebase_service.put_crypto_data(output_item)
        except Exception as e:
            print(f"Error writing to Firebase: {e}")  # Handle and print any errors related to Firebase


    def parseJsonElement( self, input_data ):
        source = input_data['source_name']
        source_type = input_data['source_type']
        date = input_data['date']
        currencies = input_data['cryptocurrency']
        title = input_data['title']
        url = input_data['url']
        text = input_data['text']

        return source, source_type, date, currencies, title, url, text

    def preprocessText( self, text ):
        return text.lower()

    def processInput(self, input_data):
        self.logger.info(f"Aggregator received input data: {input_data}")
        for input_item in input_data:
            try:
                source, source_type, date, currencies, title, url, text = self.parseJsonElement(input_item)
                self.logger.info(f"Parsed item: {input_item}")
                text = self.preprocessText(text)
    
                # Analyze sentiment
                sentiments = self.sentiment_analyzer.analyzeSentiment(currencies, title, text)
                if sentiments is None or not sentiments:
                    self.logger.warning(f"Sentiment analysis returned None or empty for: {input_item}")
                else:
                    for currency, sentiment in sentiments.items():
                        output_item = {
                            'currency': currency,
                            'source_name': source,
                            'source_type': source_type,
                            'date': date,
                            'title': title,
                            'url': url,
                            'sentiment': sentiment
                        }
                        self.writeToDatabase(output_item)
            except Exception as e:
                self.logger.error(f"Error processing input item {input_item}: {e}")

    # Continue trying to read data from the pipe until Ctrl-C is pressed
    def run( self ):
        try:
            while True:
                input_data = self.in_pipe.read()  
                if input_data is not None:
                    self.processInput( input_data )
                else:
                    print( "Waiting for data" )
                    # Not the best practice, but sleep for one second before trying to read more data.
                    sleep(1.0)

        except KeyboardInterrupt:
            pass
        

    def __init__( self, name, in_pipe, firebase_service ):
        self.logger = logging.getLogger(self.__class__.__name__)
        print( f"{name} initializing" )
        self.name = name
        self.in_pipe = in_pipe
        self.sentiment_analyzer = SentimentAnalyzer()
        self.firebase_service = firebase_service
        print( f"{name} initialized" )
