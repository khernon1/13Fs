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

## Issues - code
Some holdings had different fields. 
1. On each run, the code creates a list containing the column headers and aligns each field in the column of that specific header when writing to the file. For instance, putCall was in some holdings for Blackrock but not in most and the column lines remained correct.
2. The otherManagers field in some instances had a comma-delimited list which caused issues when writing to the file and I removed the commas. For example, Berkshire Hathaway had some otherManagers fields as '4,8,11' and it converts it to '4 8 11' in the file (Berkshire has manager #4 for every security and according to their filing it's some guy named Warren Buffett). 
 
## Issues - non-code
Finding 13Fs by mutual fund ticker is difficult as searching by ticker typically brings you to a Trust or Advisor-level page which does not include a 13F. For instance, if you search by ticker on the $25b Vanguard Equity Income Fund Investor Shares(VEIPX), it brings you to a Vanguard Fenway Funds page. Searching for Vanguard Group Inc. is where you can find the 13F-HR. I tried many, many funds by ticker but was able to find more than enough while searching by company name to be confident in my results.
