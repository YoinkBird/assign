from pprint import pprint
from ipdb import *
debug = 0
verbose = 2
#verbose = 0
#if(debug > 0):
#perl-ish  verbose = 1 if not defined verbose

#TODO: copy table code from initDeck 
# def tableRowPrint(headerList):

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
  deck = []

  # < deck generation>
  # populate deck as if it were a real deck, not just with random cards :-)
  # populate deck with suit and rank
  if(1):
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
  if(0 and verbose == 2):
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

# < def createPlayerList>
def createHashList(amount):
  hashList = []
  for index in range(0,amount):
    hashList.append({})
  return hashList

# </def createPlayerList>

# < def getNumHand>
def getNumHand(hand):
  numCards = 0
  for suit in hand:
    numCards += len(hand[suit])
  return numCards
# </def getNumHand>

# < def printHand>
def printHand(hand):
  #print("old fashioned")
  #pprint(hand,indent=2)
  #print("new fangled")
  for suit in sorted(hand):
    import sys
    sys.stdout.write(suit + ':')
    pprint(hand[suit])
# </def printHand>


# print dict sorted for easier viewing
def printDictSorted(dict):
  tmpDict = dict;
  for keys in sorted(dict):
    pprint(sorted(dict[keys]))



# main
# create a deck of 52 cards
deckLength = 52
gofishDeck = initDeck(52)

#import gofish1
#from gofish1 import *
from gofish1 import getCard
from gofish1 import drawCard

# invent some players - for now only one is needed
playerList = ["johny","barker","sally","sushmita"]
if 0:
  playerHand = {};
  playerHand2 = {};
  playerHand3 = {};
  playerHand4 = {};
#TODO : create a player class and instantiate 4 players

# seemingly currently broken; do not increase! does not affect things anyway
numPlayas = 4
handList = createHashList(numPlayas)

#test1 - does 'drawCard' work for 52 consecutive cards
#for i in range(0,52): ## 52 is one longer, causes an error, and therefore rules out incomplete loop as the cause
while gofishDeck:
  index = 0
  for playerHand in handList:
  #for playerHand in createHashList(numPlayas):
    #print("####################")
    numCardsPrev = getNumHand(playerHand)
    #print(numCardsPrev)
    #printHand(playerHand)
    #note: playerHand and playerHandPrev get updated this way, but for the deletion only playerHand is updated...
    #playerHandPrev = playerHand.copy()
    import copy
    playerHandPrev = copy.deepcopy(playerHand)
    drawCard(playerList[index],gofishDeck,playerHand)
    # test size of hand 
    numCardsPost = getNumHand(playerHand)
    # either one card was added or four cards were removed
    if((numCardsPost != numCardsPrev + 1) and (numCardsPost - numCardsPrev != 4)):
      print("-E-: hand seems to have had either more than one card added or other than 4 cards removed.")
      print("-I-: Manually compare the following to pinpoint the error")
      print("-I-: previous values:")
      # did not expose a bug with copy
      #print("number of cards: " + str(numCardsPrev))
      print("number of cards: " + str(getNumHand(playerHandPrev)))
      print("hand:")
      printHand(playerHandPrev)
      print("-I-: current values:")
      print("number of cards: " + str(numCardsPost))
      print("hand:")
      printHand(playerHand)
    #index += 1
#set_trace()
# calculate total number of cards
totCards = 0
for player in handList:
  #totCards += len(handList[player])
  totCards += getNumHand(player)
print("total cards: " + str(totCards))
if(totCards != deckLength):
  print("-I-: deck had cards subtracted!")
# check if total number divisible by 4, the number of cards discarded for a successful match
if((totCards % 4) != 0):
  print("-E-: deck seems to have had more/less cards removed than 4, the number of cards legally removable in go-fish")


index = 0
for pHand in handList:
  print(playerList[index])
  printHand(pHand)
  #pprint(pHand,indent=2)
  index += 1

# technique for printing dict as indented structure
if(0):
  import json
  print json.dumps(playerHand, sort_keys=True, indent=4)

# leave this here for debugger to run to
print


### tips
## print without newline. only accepts one arg, no lists etc.
  #import sys
  # sys.stdout.write()
