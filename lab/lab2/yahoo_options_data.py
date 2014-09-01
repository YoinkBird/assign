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
    headerList = []
    # | Strike | Symbol | Last | Chg | Bid | Ask | Vol | Open Int |
    for header in (table.findAll('th',attrs={'class':'yfnc_tablehead1','scope':'col'})):
    #for header in (table.findAll("th",class_="yfnc_tablehead1",scope_="col")):
      headerList.append(header.get_text())
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
    #</table row>

    # add header row to table
    rowList.insert(0, headerList)
    if(0):
      print("read in these rows:")
      #print(' | '.join(headerList))
      for row in rowList:
        print row

    #<verify table correctness>
    # ensure that all rows have same number of cells
    # 0th row is header row; using this to define correct number of cells
    rowSize = len(rowList[0])
    for row in rowList:
      rowLen = len(row)
      msgStr = ""
      msgStr += ("     length - expected: " + str(rowSize) + " found: " + str(rowLen))
      if(rowLen != rowSize):
        msgStr = ("-E-: row length mismatch") + msgStr
        print(msgStr)
      elif(0):
        msgStr = ("-I-: row length match") + msgStr
        print(msgStr)
    #</verify table correctness>

  return rowList
#</def parseFile>

#<def getCurrPrice>
#price is in time_rtq_ticker
# html code:
# <span class="time_rtq_ticker"><span id="yfs_l84_aapl">95.82</span></span>
def getCurrPrice(filename):
  soup = BeautifulSoup(open(filename))
  currPriceList = []
  for spanrtq in soup.find_all("span",attrs={'class' : 'time_rtq_ticker'}):
    currPriceList.append(spanrtq.get_text())
    
  print
  return currPriceList[0]

#</def getCurrPrice>

#<def getDateUrls>
# dateUrls
# <td> View By Expiration:
def getDateUrls(filename):
  soup = BeautifulSoup(open(filename))
  # find yfncsumtab and then td with 'View By Expiration'
  dateUrlMarkerText = "View By Expiration: "
  # hold the date URLs
  dateUrlList = []
  # <find correct table>
  for table in soup.find_all("table",id="yfncsumtab"):
    # find 'View By Expiration'
    for dateUrlMarkerMatch in soup.find_all(text=re.compile(dateUrlMarkerText)):
      # find parent of the dateUrlMarkerMatch element
      # this will contain all of the required 'a href'
      dateUrlContainer = dateUrlMarkerMatch.findParent()
      # list all direct 'a' underneath the parent element of the 'View by Expiration" text
      # debug: check length
      len(dateUrlContainer.findChildren('a',href=True,recursive=False))
      for link in (dateUrlContainer.findChildren('a',href=True,recursive=False)):
        dateUrlList.append(link.get('href'))

  # </find correct table>
  #TODO: this is hack because locally rendered file does not have proper url
  if(1):
    parentUrl = 'http://finance.yahoo.com'
    dateUrlListTmp = []
    for link in dateUrlList:
      #link = parentUrl + '/' + link # href already has leading slash
      link = re.sub('&','&amp;',link)
      dateUrlListTmp.append(parentUrl + link)
  dateUrlList = dateUrlListTmp
  return dateUrlList
#</def getDateUrls>

def contractAsJson(filename):
  parseFile(filename)
  quoteDataDict = {}
  quoteDataDict['currPrice'] = getCurrPrice(filename)
  quoteDataDict['dateUrls']  = getDateUrls(filename)
  jsonQuoteData = "[]"
  return jsonQuoteData
