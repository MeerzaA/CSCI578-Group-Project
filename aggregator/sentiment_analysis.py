from transformers import pipeline
from time import sleep
import json
import stanza
import re

# Placeholder class for web crawler
class Crawler:

    def send( self, item ):
        self.out_pipe.write( item )
        
    # Just send all the hard-coded data to the output pipe
    def run( self ):
        json_elements = self.data['Scraped_Format']
        self.send( json_elements )
        print( f"{self.name} exiting")

    def __init__( self, name, out_pipe ):
        print( f"{name} initializing" )
        self.name = name
        #self.data = "This is a segment from the Lightspeed newsletter. To read full editions, subscribe . As some of you may know, I host the Lightspeed podcast in addition to writing this newsletter. The conversations on that show often inspire some of the things we cover here, and I want to bring Lightspeed readers in on some of those threads. So to cap off this holiday week, here are a few recent moments from the show that have been on my mind while writing these newsletters: “Execution is the only moat, always.” — Anatoly Yakovenko , co-founder of Solana My co-host Mert Mumtaz recently grilled Solana’s chief architect on looming questions and problems the network could face in the future. It’s worth a listen . At one point in the episode, Mert asked Yakovenko what Solana’s moat could be in a world where new layer-1s and layer-2s come to market that make blockchains fast and blockspace cheap, slimming Solana’s current edge. Yakovenko’s answer pretty much boils down to: Keep executing. He also talks about hiring at Solana for tech people rather than academics, because the former are better able to work in a pressure cooker and ship features fast. “We want to understand the causal connection to things, it’s in our nature to do that. But in a market there is no causal connection it’s literally like, ‘Are there more buyers than sellers?’” — Joe McCann , CEO and CIO at Asymmetric Capital Newsletter Subscribe to Lightspeed Newsletter Subscribe McCann said this while disagreeing with me about the impact of memecoins on SOL’s price, but since I am eminently humble, I’m including it here anyways. I like what McCann is saying here because despite all the endless market analysis and tea leaves reading you’ll see in the media and online, sometimes it’s ultimately indecipherable why markets do what they do. When the price goes up, it’s because the market has more buy volume than sell volume. Identifying the buyers and sellers and their motivations are an inexact science at best. “Issuance is a cost to non-stakers. They do not receive that [issuance]. Stakers do … there is a value transfer from non-stakers to stakers.” — Dan Smith , data lead at Blockworks Research I’ve been growing increasingly interested in how value flows around the Solana ecosystem. When the price of SOL goes up, and as time passes, different stakeholders are rewarded differently. Many Solana watchers, including this newsletter , have debated if SOL’s inflation should be brought down. Inflation is dilutive, and disinflation can be bullish for an asset’s price, the thinking goes — likely influenced by the Bitcoin halving. But in Solana, issuance only dilutes non-stakers, because newly minted SOL goes to validators, and validators pass it on to stakers. “ I always like that framing which is just create a new category and go after a small market that you think will grow” — Mert Mumtaz , CEO of Helius The layer-1 wars and endless debates about which blockchain is best become very tiresome after a while. I liked the point Mert made on a recent episode though: To compete in crypto, you need to go after a meaningfully new market or use case. SOL shouldn’t be cast as an ETH killer. It’s a different blockchain that makes different tradeoffs. And Monad, Berachain, MegaETH, and the rest of them shouldn’t try to be SOL killers. They should pick a different axis upon which they can meaningfully outperform Solana. “ I don’t think it’s really workable, sadly.” — Rune Christensen , co-founder of Sky Christensen, the co-founder of Sky (formerly Maker), is referring to futarchy here, which is a buzzy new governance concept in the Solana world. Futarchy has markets, rather than voters, decide what a DAO should do. I was curious to get Christensen’s take on it because DAO governance has always been a struggle, and MakerDAO is one of the oldest examples. Christensen is basically bearish on futarchy because he thinks collective wisdom is wrong, and DAOs need someone smart who can decipher the difference between a good marketing initiative and a ponzi scheme, for instance. This sounded a bit like a pitch for traditional corporate governance to me, but what do I know? Start your day with top crypto insights from David Canellis and Katherine Ross. Subscribe to the Empire newsletter . Explore the growing intersection between crypto, macroeconomics, policy and finance with Ben Strack, Casey Wagner and Felix Jauvin. Subscribe to the Forward Guidance newsletter . Get alpha directly in your inbox with the 0xResearch newsletter — market highlights, charts, degen trade ideas, governance updates, and more. The Lightspeed newsletter is all things Solana, in your inbox, every day. Subscribe to daily Solana news from Jack Kubinec and Jeff Albus."
        

        # Combination  of positive, negative, and neutral data. Some are attempts to fool the model. "Bitcoin is the shit" fools the current default model.
        #self.data = [["I love bitcoin.", "Bitcoin blows"], ["Bitcoin is the absolute best at being the worst possible thing."], ["Bitcoin is the shit.", "How do I buy Bitcoin?"] ]
        filename = "scrape_results/reddit-2024-12-01.json" 
        with open( filename, "r") as file:
            self.data = json.load(file)

        print( f"{name} loaded data." )
        self.out_pipe = out_pipe
        print( f"{name} initialized" )
        
#TODO: move to config file
default_sentiment_model = "cardiffnlp/twitter-roberta-large-topic-sentiment-latest" 
#default_summarizer_model = "human-centered-summarization/financial-summarization-pegasus"#facebook/bart-large-cnn"
default_summarizer_model = "google/pegasus-x-large"#"human-centered-summarization/financial-summarization-pegasus"
from transformers import AutoTokenizer, PegasusXModel,PegasusTokenizer, PegasusXForConditionalGeneration

key_map = { 'BTC':'Bitcoin', '@BTC':'Bitcoin','Bitcoin':'Bitcoin', 'ETH':'Ethereum', '@ETH':'Ethereum', 'Ethereum':'Ethereum', 'SOL':'Solana', '@SOL':'Solana', 'Solana':'Solana' }
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
            return None
            #summaries = self.text_summarizer.summarize_text( input_text )
            #input_text = summaries[0]['summary_text']

        found_topics = self.find_topics_strings( input_text )

        sentiments = init_dict( found_topics )
        for topic in found_topics: 
            text_to_analyze = self.create_query( topic, input_text )
            sentiment_output = self.sentiment_pipeline( text_to_analyze )
            sentiments[key_map[topic]] = self.generateSentimentValue( sentiment_output[0] )
        #print( sentiments ) 
        return sentiments 


    def find_topics_strings( self, text ):
        target_topics = ['BTC', 'ETH', "SOL", "Bitcoin", "Ethereum", "Solana"]

        found_topics = []
        for topic in target_topics:
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

    def processInput( self, input_data ):

        for input_item in input_data:
           source, source_type, date, currencies, title, url, text = self.parseJsonElement( input_item )

           text = self.preprocessText( text )

           sentiments = self.sentiment_analyzer.analyzeSentiment( currencies, title, text )
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
