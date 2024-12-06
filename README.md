# Crypto Board 

CryptoBoard is a website that scrapes data from various news and social media sites,
and displays to the user the graphs and other data in order to gauge popularity of certain cryptos.

## Table of Contents
1. [Container Deployment](#deployment)
2. [Installation From Source](#installation)
3. [Source Code Description](#sourcecode)

## Deployment
---

# Load the Docker image:

docker load < csci578groupproject.tar.gz

# Run the container:
docker run --rm -it -p 4000:4000/tcp -p 5000:5000/tcp -p 5001:5001/tcp -p 5173:5173/tcp -p 8080:8080/tcp -p 8085:8085/tcp -p 9000:9000/tcp -p 9005:9005/tcp -p 9099:9099/tcp -p 9199:9199/tcp csci578groupproject:latest 

Note:
The front end will start quickly, but the backend will take some time to initialize. Because the database is already partially populated, you can visit the web page immediately. When the back end has initialized, the web crawlers will begin finding new data for analysis, resulting in new database entries. The front end will see these new entries and update accordingly.

# Visit the web page:

From a web browser, visit http:\\localhost:5173



## Installation

Guideline on running the Docker image to launch the website

```bash
# Clone the repository
git clone https://github.com/MeerzaA/CSCI578-Group-Project.git

# Navigate to the project directory
cd CSCI578-Group-Project

# Build the docker image 
docker-compose build

# Run the project
docker-compose up

# Access the site locally in a web browser
http://localhost:5173
```
---

## Description of source code
Backend:
- The aggregator module consists of FireBase.py and sentiment_analysis.py.
    - Firebase.py is responsible for establishing the connection between the instance and the Firebase database, as well as getting and setting data. 
    - sentiment_analysis.py is responsible for various tasks, including sentence summarizer, sentiment analyzer, and various text processors 
- The scraper module consists of two types of scrapers - Scrapy for news sources and PRAW for reddit.
    - We use Scrapy to scrape two news sources for data about various cryptocurrencies
    - We use the PRAW library to scrape Reddit's CryptoCurrency subreddit for recent posts and comments that mention a particular cryptocurrency
    
Frontend:
- The frontend was made using React and Vite, and mainly lives in the hosting directory.
- Within the subdirectory are various components necessary to make the frontend, such as firebase, which is responsible for establishing a connection with the database for the frontend.
- The project also includes UI elements, such as tables, buttons, and breadcrumbs, as well as CCS for styling.
