from lxml import etree
import xmltodict
import urllib2
import csv
import collections
import re
import pdb

class Get13Fs:

  def __init__(self):
    self.get_data()

  def get_data(self):
    url = ('https://www.sec.gov/Archives/edgar/data/812295/000114036116085960/0001140361-16-085960.txt')

    parser = etree.XMLParser(recover=True) # recover from bad characters
    data = urllib2.urlopen(url) # open site
    root = etree.fromstring(data.read(), parser=parser) #parse the response data
    
    # master dict or list of holdings and column headers
    headers = []
    comp_info = []
    all_holdings_dict = collections.OrderedDict()
    
    for element in root.iter():
      if element.tag == 'ACCEPTANCE-DATETIME': 
        self.get_filing_info(element, comp_info) # adds company info
      elif element.tag == '{http://www.sec.gov/edgar/document/thirteenf/informationtable}infoTable':
        self.add_one_holding(element, all_holdings_dict, headers) # adds data for one security
        
    # once all data is in the dict, create file
    self.build_file(all_holdings_dict, headers, comp_info)

  def add_one_holding(self, element, all_holdings_dict, headers):
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
    all_holdings_dict[str(len(all_holdings_dict))] = one_holding_list

  def add_header(self, holding, headers):
    # will add new header values if there are any
    # example: putCall was included on some 13Fs but not all
    # headers will be used later when writing to csv
    if headers == []:
      headers.append(holding.keys())
    else:
      for key in holding.keys():
        if key not in headers[0]:
          headers[0].append(key)

  def get_filing_info(self, element, comp_info):
    # used regex to parse
    comp_data = re.findall(r'(\S[^:]+):\s*(.*\S)', element.text)
    comp_info.append([item[1] for item in comp_data if item[0] == 'COMPANY CONFORMED NAME'])
    comp_info.append([item[1] for item in comp_data if item[0] == 'CONFORMED PERIOD OF REPORT'])

  def build_file(self, all_holdings_dict, headers, comp_info):
    with open('data.csv', 'wb') as f:
      writer = csv.writer(f)
      
      for item in comp_info: # add filing info to file
        writer.writerow([''.join(item)])
            
      for line in headers: # add headers to file  
        writer.writerow(['\t'.join(line)])

      # values will be added based off the index of the header
      # so that everything is in the correct columns      
      for line in all_holdings_dict.values():
        write_line = []
        self.conditionally_add_line(line, headers, write_line)

        # exports tab delimited as requested
        # easily copies to a spreadsheet
        writer.writerow(['\t'.join(write_line)])
    f.close()

  def conditionally_add_line(self, line, headers, write_line):    
    for (idx,val) in enumerate(line):          
      header_index = headers[0].index(val)

      # it won't write correctly if a list of commas are included
      # so I replace them with spaces which writes fine
      # for ex. otherManager 4,8,11 would write as 4 8 11 in that column
      if ',' in line.values()[idx]:
        write_line.insert(header_index, line.values()[idx].replace(',',' '))
      # some holdings are missing fields 
      # for instance otherManager is commonly not included on some holdings
      # this will put a blank space there and keep the columns accurate
      elif headers[0][idx] not in line.keys():
        write_line.insert(idx, ' ')
        write_line.insert(header_index, line.values()[idx])
      else:
        write_line.insert(header_index, line.values()[idx])


Get13Fs()

