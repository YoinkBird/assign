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
#  this table has one row with headers and the rest is data
def parseFile(filename):
  #soup = BeautifulSoup(open(filename))
  #if(type(filename) == "<class 'bs4.element.Tag'>"):
  soup = filename
  #pdb.set_trace()
  #note: the yahoo table nested. best strategy to find right table:
  #      drill down to the header info and get parent table
  # for now: just skip down one table
  # table_class=yfnc_datamodoutline1 [ table [ ... ] ]
  #for tableOuter in soup.find_all("table",class_="yfnc_datamodoutline1"):
  if(1):
    #print(tableOuter['class']) # this should be the yfnc_datamodoutline1
    #table = tableOuter.findNext("table")
    table = soup.findNext("table")

    #<table header>
    headerList = []
    # | Strike | Symbol | Last | Chg | Bid | Ask | Vol | Open Int |
    for header in (table.findAll('th',attrs={'class':'yfnc_tablehead1','scope':'col'})):
    #for header in (table.findAll("th",class_="yfnc_tablehead1",scope_="col")):
      headerText = header.get_text()
      #TODO: hack: json file shows 'change' whereas webpage shows 'chg'
      if(1):
        headerText = re.sub('Chg','Change',headerText)
        headerText = re.sub('Open Int','Open',headerText)
      headerList.append(headerText)

    #TODO: update the 'Symbol' names
    #  possibly easy with json; could also find all in beautifulsoup and swap out in the html
    # s/{a-Z}+[7]{0,1}/$1/
    # re.sub('AAPL.*','AAPL',headerText)

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
      # http://www.crummy.com/software/BeautifulSoup/bs4/doc/#contents-and-children
      # http://stackoverflow.com/questions/6287529/how-to-find-children-of-nodes-using-beautiful-soup/15892793#15892793
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
      # https://www.google.com/search?q=python+htmlentities
      link = re.sub('&','&amp;',link)
      dateUrlListTmp.append(parentUrl + link)
  dateUrlList = dateUrlListTmp
  return dateUrlList
#</def getDateUrls>

#<def getOptionQuotes>
# need to find 'yfnc_mod_table_title1' for the 'get' and 'put' option
# need to find 'yfnc_datamodoutline1'  for the data
# optionQuotes
# html sample:
# call/put options:
# <table class="yfnc_mod_table_title1" width="100%" cellpadding="10" cellspacing="10" border="50"><tbody><tr valign="top"><td><small><b><strong class="yfi-module-title">Call Options</strong></b></small></td><td align="right">Expire at close Friday, September 5, 2014</td></tr></tbody></table>
# data
# <table class="yfnc_datamodoutline1" width="100%" cellpadding="5" cellspacing="0" border="2">...<table>

def getOptionQuotes(filename):
  soup = BeautifulSoup(open(filename))
  # desired format is array of hashes
  optionQuoteList = []
  # find yfncsumtab and then td with 'View By Expiration'
  dateUrlMarkerText = "View By Expiration: "
  # hold the date URLs
  dateUrlList = []
  # <find_parent_table>
  for table in soup.find_all("table",id="yfncsumtab"):
    # loop through the tables
    optionType = ''
    tableTitleClass = 'yfnc_mod_table_title1'
    tableDataClass  = 'yfnc_datamodoutline1'
    #len(table.findChildren('table',class_=re.compile('yfnc_datamodoutline1|yfnc_mod_table_title1')))
    for subTable in (table.findChildren('table',class_=re.compile('yfnc_datamodoutline1|yfnc_mod_table_title1'))):
      # grab title first 
      # find the 'Call|Put Options'
      # flexible: user lowercase version of first letter of match
      className = subTable['class']
      # I don't like doing it this way but python regexes and bs4 are driving me crazy
      #   really hard to just get a class-name or a string or anything else :-(
      if(subTable['class'][0] == tableTitleClass):
        for textMatch in (subTable.find_all("td",text=re.compile('.*Options'))):
          # get the text-value, then the first char
          # I don't like doing it this way but python regexes and bs4 are driving me crazy
          #   really hard to just get a class-name or a string or anything else :-(
          #optionType = textMatch.get_text()[0].lower() # no need to lowercase it
          optionType = textMatch.get_text()[0]
      # make sure the tables are iterating in the right order:
      #  check that the 'optionType' is correctly set, and clear it when done
      if(subTable['class'][0] == tableDataClass and (optionType == 'C' or 'P')):
        # pass to the 'parseFile' subroutine
        optionQuoteListTmp = parseFile(subTable)
        optionQuoteListTmp = addHeaderName(optionQuoteListTmp,{'Type':optionType})
        # < regex_replace>
        # mini contract:
        # http://www.cboe.com/Products/indexopts/mini_spec.aspx
        # The option symbol for Mini Options shall be the underlying security symbol followed by the number "7"
        # find symbol 'AAPL' or 'AAPL7' and hard-code replace for testing
        symbolIndex = optionQuoteListTmp[0].index('Symbol')
        replaceValues(optionQuoteListTmp,symbolIndex,'(\D+[7]{,1}).*',r'\1')
        # </regex_replace>

        optionQuoteListTmp = convert_2d_list_to_list_of_dicts(optionQuoteListTmp)

        #print("-I-: adding " + str(len(optionQuoteListTmp)) + " elements")
        optionQuoteList.extend(optionQuoteListTmp)
        # populate optionQuoteList
        # clear optionType to make sure it gets set properly
        optionType = ''
  # </find_parent_table>
  return optionQuoteList
#</def getOptionQuotes>

#< def convert_2d_list_to_list_of_dicts>
# map list[0] as keys, list[1-len(list] as values
def convert_2d_list_to_list_of_dicts(twoDList):
  # hold dicts
  dataDictList = []
  # zeroth row is header and defines keys
  for rowIndex in range(1,len(twoDList)-1):
    # loop through values
    tempDict = {}
    #for colIndex in range(0,len(twoDList[rowIndex])-1):
    for colIndex in range(0,len(twoDList[rowIndex])):
      tempDict[twoDList[0][colIndex]] = twoDList[rowIndex][colIndex]
    dataDictList.append(tempDict)

  #<verify dataDictList correctness>
  # ensure that all dicts have same number of keys 
  # simply checking that all dicts are same size
  #dictNumKeysAbs = len of first found dict
  # TODO: verify values
  dictNumKeysAbs = -1
  dictNumValAbs = -1
  msgStr = "checking integrity of data structure: array of dicts\n"
  for dict in dataDictList:
    dictNumKeys = len(dict)
    dictNumVal = len(dict.keys())
    # initial setting
    if(dictNumKeysAbs < 0):
      dictNumKeysAbs = dictNumKeys
    if(dictNumValAbs < 0):
      dictNumValAbs = dictNumVal
    msgStrTmp = ("     keys   - expected: " + str(dictNumKeysAbs) + " found: " + str(dictNumKeys))
    msgStrTmp += ("     values - expected: " + str(dictNumValAbs) + " found: " + str(dictNumVal))
    if(dictNumKeys != dictNumKeysAbs):
      msgStr = msgStr + "-E-: dict key/value mismatch" + msgStrTmp
      print(msgStr)
    elif(0):
      msgStr = msgStr + "-I-: dict key/value match" + msgStrTmp
      print(msgStr)
    msgStr = "" # clear it 
  #</verify dataDictList correctness>
  return dataDictList

#</def convert_2d_list_to_list_of_dicts>


#< def addHeaderName>
# add header to table
def addHeaderName(table,headerDict):
  for newHeader in headerDict:
    # zeroth row defines headers
    table[0].append(newHeader)
    for index in range(1,len(table)):
      table[index].append(headerDict[newHeader])

  #<verify table correctness>
  # ensure that all rows have same number of cells
  # 0th row is header row; using this to define correct number of cells
  rowSize = len(table[0])
  for row in table:
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
  return table
    
#</def addHeaderName>

#< def replaceValues>
# replace values in column for a given header
def replaceValues(table,valueIndex,matchExpr,replExpr):
  for index in range(1,len(table)):
    #newValue = re.sub('(AAPL[7]{,1}).*',r'\1',table[index][valueIndex])
    newValue = re.sub(matchExpr,replExpr,table[index][valueIndex])
    #print('-I-: changing ' + table[index][valueIndex] + ' to ' + newValue)
    table[index][valueIndex] = newValue

  #<verify table integrity>
  # ensure that all rows have same number of cells
  # 0th row is header row; using this to define correct number of cells
  rowSize = len(table[0])
  for row in table:
    rowLen = len(row)
    msgStr = ""
    msgStr += ("     length - expected: " + str(rowSize) + " found: " + str(rowLen))
    if(rowLen != rowSize):
      msgStr = ("-E-: row length mismatch") + msgStr
      print(msgStr)
    elif(0):
      msgStr = ("-I-: row length match") + msgStr
      print(msgStr)
  #</verify table integrity>
  return table
#</def replaceValues>

def contractAsJson(filename):
  #refactored to work with getOptionQuotes: parseFile(filename)
  quoteDataDict = {}
  quoteDataDict['optionQuotes'] = getOptionQuotes(filename)
  quoteDataDict['currPrice'] = getCurrPrice(filename)
  quoteDataDict['dateUrls']  = getDateUrls(filename)
  jsonQuoteData = "[]"
  return jsonQuoteData
