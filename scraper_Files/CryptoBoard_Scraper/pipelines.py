# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import sys


# for docker we might need to make sure that the import from aggregator is reconized 
# for example we might neeed to set a PYTHONPATH in scrapy.cfg of path home/project_root/aggregator or export PYTHONPATH=....
# It has crashed for the 100th time, I am going to have to help it find the root no matter the enviroment 
# Once we are in docker we need to make sure that Crypto-Board-CSCI578-Project is always the root 
#   and that we only need to go back 2 levels get to it.
'''
For example 
    PS S:\Documents\GitHub\CSCI_578\Project\Crypto-Board-CSCI578-Project\scraper_Files\CryptoBoard_Scraper> cd ..
    PS S:\Documents\GitHub\CSCI_578\Project\Crypto-Board-CSCI578-Project\scraper_Files> cd ..
    PS S:\Documents\GitHub\CSCI_578\Project\Crypto-Board-CSCI578-Project> 
'''

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

#print(f"PROJECT_ROOT: {PROJECT_ROOT}")
#print(f"sys.path: {sys.path}")

from aggregator import Aggregator
from aggregator import FirebaseService
from aggregator import DataPipe
import logging

class CryptoboardScraperPipeline:

    def process_item(self, item, spider):
        print('PROCESS ITEM!!!')
        spider.out_pipe.write( item )
        return item

