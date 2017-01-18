# import requests
# from bs4 import BeautifulSoup
# import pdb

# url = 'https://www.sec.gov/Archives/edgar/data/728100/000093041316008673/0000930413-16-008673.txt'
# page = requests.get(url)
# page_text = page.text

from string import strip
import xmltodict
import urllib2
import untangle
import pdb
import itertools

import xml.etree.ElementTree as ET
from lxml import etree
from xml.dom import minidom
import json

url = ('https://www.sec.gov/Archives/edgar/data/1166559/000110465914039387/0001104659-14-039387.txt')

parser = etree.XMLParser(recover=True) # recover from bad characters
data = urllib2.urlopen(url)
root = etree.fromstring(data.read(), parser=parser)
for element in root.iter():
  if element.tag == '{http://www.sec.gov/edgar/document/thirteenf/informationtable}infoTable':
    doc = xmltodict.parse(etree.tostring(element))
    print_list = []
    for item in doc['infoTable'].items():      
    # merged = list(itertools.chain(*doc['infoTable'].values()))
    # json_str = json.dumps(doc['infoTable'])
    # json_dict = json.loads(json_str)
    # print doc['infoTable']['cusip']
      if isinstance(item[1], dict):
        print_list.append(item[1].values())
      else:
        print_list.append([item[1]])
    # flatten nested list 
    merged = [val for sublist in print_list for val in sublist]
    # pdb.set_trace()
    print ('\t'.join(merged[2:-1]))
    



