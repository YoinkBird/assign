import random
from ipdb import *
from IPython import get_ipython
ipython = get_ipython()

tList = [0.01,0.1,1]
tResultsDict = {}

# check curTime.best
# cli example: 
#  curTime = %timeit -r1 -n1 -o sorted([random.random() for rand in xrange(100000)])
curTimeDemo = ipython.magic("timeit -r1 -n1 -o sorted([random.random() for rand in xrange(100000)])")

#TODO: set one multiplier, use in both blocks
# ie. multiplier = 0.8
# numRandom = int(numRandom * (1 + (1 - multiplier ))) # numRandom *= 1.1
# numRandom = int(numRandom * (1 + (    multiplier ))) # numRandom *= 0.9
#< loop over times>
for t in tList:
  upperRange = t * 1.1
  lowerRange = t * 0.9
  # start with 100k numbers
  numRandom = 100000
  notdone = 1
  while notdone:
#    set_trace()
    print("using " + str(numRandom) + " random floats")
    curTime = ipython.magic("timeit -r1 -n1 -o sorted([random.random() for rand in xrange(" + str(numRandom) + ")])")
    if(curTime.best < t):
      # generate longer list
      print("smaller:" + str(curTime.best) + " < " + str(t))
      multplier = t / curTime.best
      multplier = 1.09
      numRandom = int(numRandom * multplier)
      if(curTime.best > lowerRange):
        notdone = 0
    elif(curTime.best > t):
      print("bigger:" + str(curTime.best) + " > " + str(t))
      #set_trace()
      multplier = t / curTime.best
      multplier = 0.9
      numRandom = int(numRandom * multplier)
      if(curTime.best < upperRange):
        notdone = 0
      #notdone = 0
    elif(curTime.best == t):
      print("just right:" + str(curTime.best) + " == " + str(t))
      # exit this loop
      notdone = 0
    #print(curTime.best)
    print("")
  tResultsDict[t] = {'realtime':curTime.best, 'listSize':numRandom}
#</loop over times>
#set_trace()
import pprint
for tresult in sorted(tResultsDict):
  print("time: " + str(tresult) + " random numbers: " + str(tResultsDict[tresult]))
print
pprint.pprint(tResultsDict)
