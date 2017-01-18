import xmltodict
import urllib2
import pdb
import csv
from lxml import etree
import collections

class Get13Fs:

  def __init__(self):
    self.get_data()

  def get_data(self):
    ### turn into list and iter it
    url = ('https://www.sec.gov/Archives/edgar/data/1029160/000114036116086458/0001140361-16-086458.txt')

    parser = etree.XMLParser(recover=True) # recover from bad characters
    data = urllib2.urlopen(url) # open site
    root = etree.fromstring(data.read(), parser=parser) #parse the response data
    
    # master dict or list of holdings and column headers
    headers = []
    all_holdings_list = collections.OrderedDict()
    
    for element in root.iter(): # find where the security info begins
      if element.tag == '{http://www.sec.gov/edgar/document/thirteenf/informationtable}infoTable':
        self.add_one_holding(element, all_holdings_list, headers)
        
    # once all data is in the dict, create file
    self.build_file(all_holdings_list, headers) 

  def add_one_holding(self, element, all_holdings_list, headers):
    # prefer to parse the element tree by converting to a dictionary
    doc = xmltodict.parse(etree.tostring(element))
    # will convert values to this dict in the format I want    
    one_holding_list = collections.OrderedDict()
    for item in doc['infoTable'].items(): 
      if isinstance(item[1], dict): # deals with nested elements
        for value in item[1]:
          # includes main header for anything nested
          # along with the nester header for ease of viewing
          str_val = "{0} - {1}".format(item[0], value)
          one_holding_list[str_val] = item[1][value]
      elif '@xmlns' in item[0]: # no need to store this data
        continue
      else:      
        one_holding_list[item[0]] = item[1] # not nested

    # call function to check and/or add column 
    # header values for the individual holding
    self.add_header(one_holding_list, headers)
    # add holdings data to master dict
    all_holdings_list[str(len(all_holdings_list))] = one_holding_list

  def add_header(self, holding, headers):
    # will add new header values if there are any
    # example: putCall was included on only one 13F I checked
    # headers will be used later when writing to csv
    if headers == []:
      headers.append(holding.keys())
    else:
      for key in holding.keys():
        if key not in headers[0]:
          headers[0].append(key)

  def build_file(self, all_holdings_list, headers):
    # how to create file
    # include fund name and stuff at top 
    # concatentate name and date
    with open('data.csv', 'wb') as f:
      writer = csv.writer(f)
      # add headers to file
      for line in headers:
        writer.writerow(['\t'.join(line)])

      # values will be added based off the index of the header
      # so that everything is in the correct columns
      for line in all_holdings_list.values():
        write_line = []
        for (idx,val) in enumerate(line):
          header_index = headers[0].index(val)
          write_line.insert(header_index, line.values()[idx])

        writer.writerow(['\t'.join(write_line)])
    f.close()

Get13Fs()
