from transformers import pipeline
import sys


def Aggregator():
    sentiment_pipeline = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")
    data = ["I love bitcoin.", "Bitcoin blows", "Bitcoin is the absolute best at being the worst possible thing."]

    for out in sentiment_pipeline(data):
        print(out)

def main():
    Aggregator()
    
if __name__ == '__main__':
    sys.exit(main())