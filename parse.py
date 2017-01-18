import xmltodict
import urllib2
import pdb
import csv
from lxml import etree
import collections

class Get13Fs:

  def __init__(self):
    # self.all_holdings_list = []  
    self.all_holdings_list = collections.OrderedDict()
    self.headers = []
    self.url = ('https://www.sec.gov/Archives/edgar/data/728100/000093041316008673/0000930413-16-008673.txt')
    self.get_data()

  def get_data(self):
    parser = etree.XMLParser(recover=True) # recover from bad characters
    data = urllib2.urlopen(self.url) # open site
    root = etree.fromstring(data.read(), parser=parser) #parse the response data

    counter = 0
    for element in root.iter():
      if element.tag == '{http://www.sec.gov/edgar/document/thirteenf/informationtable}infoTable':
        # if counter == 0: self.add_header(element)
        self.add_one_holding(element)
        counter += 1

    # self.add_header()
    self.build_file()
  
  def add_header(self, holding):
    # pdb.set_trace()    
    if self.headers == []:
      self.headers.append(holding.keys())
    else:
      for key in holding.keys():
        if key not in self.headers[0]:
          self.headers[0].append(key)          
    #   temp = {}
    #   temp['headers'] = holding.keys()
    #   self.headers.update(temp)
    
    # else:
      # self.headers['headers'].update(holding.keys())  

    # self.all_holdings_list[0]    
    # for item in self.all_holdings_list.items():
    #   item[1].keys()
      


    # doc = xmltodict.parse(etree.tostring(element))
    # one_holding_list = []
    # for item in doc['infoTable'].items():      
    #   if isinstance(item[1], dict):
    #     one_holding_list.append(item[1].keys())
    #   elif '@xmlns' in item[0]:
    #     continue
    #   else:
    #     one_holding_list.append([item[0]])
    # self.all_holdings_list.append(one_holding_list)


  def add_one_holding(self, element):
    doc = xmltodict.parse(etree.tostring(element))
    one_holding_list = collections.OrderedDict()
    for item in doc['infoTable'].items():
      if isinstance(item[1], dict):
        for value in item[1]:
          # includes main header for nested xml
          str_val = "{0} - {1}".format(item[0], value)
          one_holding_list[str_val] = item[1][value]
          # one_holding_list.update(item[1])
      elif '@xmlns' in item[0]:
        continue
      else:
        # if item[0] in (y for x in self.all_holdings_list[0] for y in x):        
        one_holding_list[item[0]] = item[1]
        # one_holding_list.append([item[1]])
    # self.all_holdings_list.update(one_holding_list)
    issuer = one_holding_list['cusip']
    self.add_header(one_holding_list)
    self.all_holdings_list[issuer] = one_holding_list

  def build_file(self):
    with open('data.csv', 'wb') as f:
      writer = csv.writer(f)
      # add headers
      for line in self.headers:
        writer.writerow(['\t'.join(line)])

      for line in self.all_holdings_list.values():
        write_line = []
        for (idx,val) in enumerate(line):
          header_index = self.headers[0].index(val)
          write_line.insert(header_index, line.values()[idx])
        # merged = [val for sublist in line for val in sublist]
        writer.writerow(['\t'.join(write_line)])
      # for line in self.all_holdings_list.values():
      #   writer.writerow(['\t'.join(line['cusip'])])
    f.close()
    

Get13Fs()

