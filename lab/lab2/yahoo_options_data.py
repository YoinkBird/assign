import json
import sys
import re
import urllib 
from bs4 import BeautifulSoup
#import pdb
from ipdb import set_trace
#NOTE: 
# table syntax
# | Strike | Symbol              | Last  | Chg  | Bid   | Ask   | Vol | Open Int |
# | 50.00  | AAPL140920C00050000 | 46.70 | 0.00 | 45.90 | 46.35 | 1   | 1        |
'''
# find all tables with the 'datamodoutline1'
for table in soup.find_all("table",class_="yfnc_datamodoutline1"):
  print(table['class'])
'''
def parseFile(filename):
  soup = BeautifulSoup(open(filename))
  #pdb.set_trace()
  #note: the yahoo table nested. best strategy to find right table:
  #      drill down to the header info and get parent table
  # for now: just skip down one table
  # table_class=yfnc_datamodoutline1 [ table [ ... ] ]
  for tableOuter in soup.find_all("table",class_="yfnc_datamodoutline1"):
    #print(tableOuter['class']) # this should be the yfnc_datamodoutline1
    table = tableOuter.findNext("table")

    #<table header>
    optionQuotesList = []
    # | Strike | Symbol | Last | Chg | Bid | Ask | Vol | Open Int |
    for header in (table.findAll('th',attrs={'class':'yfnc_tablehead1','scope':'col'})):
    #for header in (table.findAll("th",class_="yfnc_tablehead1",scope_="col")):
      optionQuotesList.append(header.get_text())
    #</table header>

    #<table row>
    # loop through rows and then cells (td)
    rowList = []
    # | 50.00 | AAPL140920C00050000 | 46.70 | 0.00 | 45.90 | 46.35 | 1 | 1 |
    # rows have no attributes
    #set_trace()
    for thisRow in table.findAll("tr"): 
      # row contains either th or td
      #set_trace()
      cellList = []
      #< read cells>
      for thisCell in thisRow.findAll('td'):
        cellList.append(thisCell.get_text())
      #</read cells>
      if 0 or cellList:
        rowList.append(cellList)
    #</read rows>
    print("read in these rows:")
    print(' | '.join(optionQuotesList))
    for row in rowList:
      print row

    #</table row>
  return


def contractAsJson(filename):
  parseFile(filename)
  jsonQuoteData = "[]"
  return jsonQuoteData
