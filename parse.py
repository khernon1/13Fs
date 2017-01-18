import xmltodict
import urllib2
import pdb
import csv
from lxml import etree

class Get13Fs:

  def __init__(self):
    self.all_holdings_list = []  
    self.url = ('https://www.sec.gov/Archives/edgar/data/1029160/000114036116086458/0001140361-16-086458.txt')
    self.get_data()

  def get_data(self):
    parser = etree.XMLParser(recover=True) # recover from bad characters
    data = urllib2.urlopen(self.url) # open site
    root = etree.fromstring(data.read(), parser=parser) #parse the response data

    counter = 0
    for element in root.iter():
      if element.tag == '{http://www.sec.gov/edgar/document/thirteenf/informationtable}infoTable':
        if counter == 0: self.add_header(element)
        self.add_one_holding(element)
        counter += 1

    self.build_file()
  
  def add_header(self, element):
    doc = xmltodict.parse(etree.tostring(element))
    one_holding_list = []
    for item in doc['infoTable'].items():      
      if isinstance(item[1], dict):
        one_holding_list.append(item[1].keys())
      elif '@xmlns' in item[0]:
        continue
      else:
        one_holding_list.append([item[0]])
    self.all_holdings_list.append(one_holding_list)


  def add_one_holding(self, element):
    doc = xmltodict.parse(etree.tostring(element))
    one_holding_list = []
    for item in doc['infoTable'].items():      
      if isinstance(item[1], dict):
        one_holding_list.append(item[1].values())
      elif '@xmlns' in item[0]:
        continue
      else:
        if item[0] in (y for x in self.all_holdings_list[0] for y in x):
          pdb.set_trace()
          one_holding_list.append([item[1]])
    self.all_holdings_list.append(one_holding_list)


  def build_file(self):
    with open('data.csv', 'wb') as f:
      writer = csv.writer(f)
      for line in self.all_holdings_list:
        merged = [val for sublist in line for val in sublist]
        writer.writerow(['\t'.join(merged)])
    f.close()
    

Get13Fs()

