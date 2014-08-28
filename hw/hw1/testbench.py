from pprint import pprint
import pdb
debug = 0
verbose = 2
#verbose = 0
#if(debug > 0):
#perl-ish  verbose = 1 if not defined verbose

def tableRowPrint(headerList):
    #<table>

    # rank is first cell, highest rank is 2 digits
    # suit is second cell, longest suit is diamonds at index 2
      # TODO no point in calculating right now...
    cellWidthList = [2 , len(suitList[2])]
    # but the len('rank') bigger than any rank
    headerList = ['rank','suit']
    if(len(headerList[0]) > cellWidthList[0]):
      cellWidthList[0] = len(headerList[0])
    # calculate cellpadding
    getCellPaddingLam = lambda x,y: ' ' * (x - y)
    
    #< legacy>
    #del tableHorizRow = '-' * tableWidth
    #ver1 debugPrintStr = debugPrintStr + 'suit | rank' + '\n' + '----------' + '\n'
    #ver2 debugPrintStr = debugPrintStr + 'suit | rank' + '\n' + tableHorizRow + '\n'
    #ver3 debugPrintStr = debugPrintStr + ' suit ' + ' ' * (cellWidth - 4) + ' | rank' + '\n' + tableHorizRow + '\n'
    #ver4 debugPrintStr = debugPrintStr + ' suit' + getCellPaddingLam(cellWidth , 4) + ' | rank' + '\n' + tableHorizRow + '\n'
    #ver5 tableHeader = ' suit' + getCellPaddingLam(cellWidth , 4) + ' | rank' + '\n' + tableHorizRow + '\n'
    #ver6 tableHeader = ' suit' + getCellPaddingLam(cellWidth , 4) + ' | rank ' 
    #</legacy>

    #ver7
    # create padding for each cell
    tableHeader  = headerList[0] + getCellPaddingLam(cellWidthList[0] , len(headerList[0]))
    tableHeader += ' | ' 
    tableHeader += headerList[1] + getCellPaddingLam(cellWidthList[1], len(headerList[1]))
    tableHeader = ' ' + tableHeader + ' '
    # horizontal line to delineate header and table begin,end
    tableHorizRow = '-' * len(tableHeader)
    tableHeader = tableHorizRow + '\n' + tableHeader + '\n' + tableHorizRow + '\n'
    #< populate table>
    table = ''
    for index in deck:
      #ver1 debugPrintStr = debugPrintStr + ' | '.join(index) + '\n'
      #debugPrintStr = debugPrintStr + ' ' + index[0] + getCellPaddingLam(cellWidth,len(index[0])) + ' | ' + index [1] + '\n'
      table = table + ' ' + index[0] + getCellPaddingLam(cellWidthList[0],len(index[0])) + ' | ' + index [1] + '\n'
    #</populate table>

    table = tableHeader + table + tableHorizRow
    debugPrintStr = debugPrintStr + table + '\n'
    # </table>

def initDeck(deckSize):

  '''
  def initDeck
  purpose:
  A deck is a list that initially contains 52 elements.
  Each element of the list is a tuple with two elements: the rank and the suit.
  So a single entry in the deck might be the tuple ("K", "spades"), 
    which is the king of spades.
  '''
  rankList = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
  rankList = ["02", "03", "04", "05", "06", "07", "08", "09", "10", "JJ", "QQ", "KK", "AA"]
  suitList = ["spades", "hearts", "diamonds", "clubs"]

  # deck: list with 52 elements, each element is tuple with rank and suit
  #deck = [("k","spades")]
  deck = []
# populate deck:
# loop 1 through 52 or 0 through 51 and choose rank, suit deterministically
# deck[$index] = (rankList[$index % $len(rankList),suitList[$index % len(suitList)])
# deck.append((rankList[len(rankList)%index],suitList[len(suitList)%index]))

  # return 
  #< legacy>
  if(1):
    getRandom = lambda list,index: list[ index % (len(list) - 1)]
    # note: equ to 'for(index = 0, index < 52, index++)'
    #deckSize = 52;
    #for index in range(0,52):
    for index in range(0,deckSize):
      if(debug == 1):
        print("index",index,"\n");
      deck.append((getRandom(rankList,index),getRandom(suitList,index)))
    #</legacy>

    # found a better way to do it, remove the deck and start over

  # < deck generation>
  # populate deck as if it were a real deck, no just with random cards :-)
  # populate deck with suit and rank
  if(1):
    deck = []
    #del(deck)
    for suitTmp in suitList:
      for rankTmp in rankList:
        deck.append((rankTmp,suitTmp))
  # </deck generation>

  # < debug printing>
  # debug printing; ideally format would be: deck initialised\nprint out deck\ntotal elemetns
  debugPrintStr = ""
  if(verbose != 0):
    debugPrintStr += "deck initialised\n"
  if(verbose >= 1):
    debugPrintStr = debugPrintStr + "total elements: " + str(len(deck)) + '\n'
  if(verbose == 2):
    #<table>
    #print "total elements:" , len(deck)
    # welp, print out a quick table I guess
    #print "deck initialised:" , deck , "\n"
    #tableWidth = 15

    # rank is first cell, highest rank is 2 digits
    # suit is second cell, longest suit is diamonds at index 2
      # TODO no point in calculating right now...
    cellWidthList = [2 , len(suitList[2])]
    # but the len('rank') bigger than any rank
    headerList = ['rank','suit']
    if(len(headerList[0]) > cellWidthList[0]):
      cellWidthList[0] = len(headerList[0])
    # calculate cellpadding
    getCellPaddingLam = lambda x,y: ' ' * (x - y)
    
    #< legacy>
    #del tableHorizRow = '-' * tableWidth
    #ver1 debugPrintStr = debugPrintStr + 'suit | rank' + '\n' + '----------' + '\n'
    #ver2 debugPrintStr = debugPrintStr + 'suit | rank' + '\n' + tableHorizRow + '\n'
    #ver3 debugPrintStr = debugPrintStr + ' suit ' + ' ' * (cellWidth - 4) + ' | rank' + '\n' + tableHorizRow + '\n'
    #ver4 debugPrintStr = debugPrintStr + ' suit' + getCellPaddingLam(cellWidth , 4) + ' | rank' + '\n' + tableHorizRow + '\n'
    #ver5 tableHeader = ' suit' + getCellPaddingLam(cellWidth , 4) + ' | rank' + '\n' + tableHorizRow + '\n'
    #ver6 tableHeader = ' suit' + getCellPaddingLam(cellWidth , 4) + ' | rank ' 
    #</legacy>

    #ver7
    # create padding for each cell
    tableHeader  = headerList[0] + getCellPaddingLam(cellWidthList[0] , len(headerList[0]))
    tableHeader += ' | ' 
    tableHeader += headerList[1] + getCellPaddingLam(cellWidthList[1], len(headerList[1]))
    tableHeader = ' ' + tableHeader + ' '
    # horizontal line to delineate header and table begin,end
    tableHorizRow = '-' * len(tableHeader)
    tableHeader = tableHorizRow + '\n' + tableHeader + '\n' + tableHorizRow + '\n'
    #< populate table>
    table = ''
    for index in deck:
      #ver1 debugPrintStr = debugPrintStr + ' | '.join(index) + '\n'
      #debugPrintStr = debugPrintStr + ' ' + index[0] + getCellPaddingLam(cellWidth,len(index[0])) + ' | ' + index [1] + '\n'
      table = table + ' ' + index[0] + getCellPaddingLam(cellWidthList[0],len(index[0])) + ' | ' + index [1] + '\n'
    #</populate table>

    table = tableHeader + table + tableHorizRow
    debugPrintStr = debugPrintStr + table + '\n'
    # </table>
  if(verbose != 0):
    print(debugPrintStr)
  # </debug printing>

  return deck
## </ def initDeck() > ######################

# print dict sorted for easier viewing
def printDictSorted(dict):
  tmpDict = dict;
  for keys in sorted(dict):
    pprint(sorted(dict[keys]))



# main
# create a deck of 52 cards
gofishDeck = initDeck(52)

#import gofish1
#from gofish1 import *
from gofish1 import getCard
from gofish1 import drawCard

#awww crap...card1 = getCard(gofishDeck)

# invent some players
playerList = ["johny","barker","sally","sushmita"]
playerHand = {};
#TODO : create a player class and instantiate 4 players
debugDeck = []
#for i in range(0,52): ## 52 is one longer, causes an error, and therefore rules out incomplete loop as the cause
while gofishDeck:
  debugDeck.append(drawCard(playerList[0], gofishDeck, playerHand))

pprint(sorted(debugDeck)) 

#for player in playerList:
#  drawCard(player,gofishDeck,playerHand)
from pprint import pprint

#print("for-loop printout")
print("final hand")
for ranks in sorted(playerHand):
  #print(ranks, sorted(playerHand[ranks]))
  playerHand[ranks] = sorted(playerHand[ranks])

pprint(playerHand, indent = 1)

import json
if(0):
  print json.dumps(playerHand, sort_keys=True, indent=4)

# leave this here for debugger to run to
print
