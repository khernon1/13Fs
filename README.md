# 13Fs

## Objective
Be able to crawl a 13F-HR document from the URL and display the holdings information in a more manageable format.

## Process
All the code can be found in parser.py. I left it in one file for ease of viewing.

To run:
```
1. Clone repo and cd into directory in terminal
2. Run 'python parse.py' and it will run for the current URL
3. Change to a different URL and run again to see new results
```

## Outcome
I ran this for more than a dozen investment firms and read the SEC requirements for filing 13Fs in 12b [here](https://www.sec.gov/about/forms/form13f.pdf) and my current code should work for all.

Please see a short example video below:
![quovogif](https://cloud.githubusercontent.com/assets/17169813/22092931/7750cf32-ddcf-11e6-9a77-3f96ab640307.gif)

## Issues - code
I played around with some different ways to parse the XML and eventually settled on lxml/etree and xmltodict libraries. I liked etree as it allowed me to easily escape symbols (such as &) since the entire file is not in XML. Xmltodict was a straightforward way to iterate through the holdings and find what I need.

Some holdings had different fields.

1. On each run, the code creates a list containing the column headers and aligns each field in the column of that specific header when writing to the file. For instance, putCall was in some holdings for Blackrock but not in most and the column lines remained correct.

2. The otherManagers field in some instances had a comma-delimited list which caused issues when writing to the file and I removed the commas. For example, Berkshire Hathaway had some otherManagers fields as '4,8,11' and it converts it to '4 8 11' in the file (Berkshire has manager #4 for every security and according to their filing it's some guy named Warren Buffett). 

3. Again with otherManagers, sometimes it was given, sometimes not. I designed it to put a blank field if it is included in my list of headers but no value is in that individual holding. This logic would work for any field.

## Issues - non-code
Finding 13Fs by mutual fund ticker is difficult as searching by ticker typically brings you to a Trust or Advisor-level page which does not include a 13F. For instance, if you search by ticker on the $25b Vanguard Equity Income Fund Investor Shares(VEIPX), it brings you to a Vanguard Fenway Funds page. Searching for Vanguard Group Inc. is where you can find the 13F-HR. I tried many, many funds by ticker but was able to find more than enough while searching by company name to be confident in my results.
