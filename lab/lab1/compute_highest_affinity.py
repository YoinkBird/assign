# No need to process files and manipulate strings - we will
# pass in lists (of equal length) that correspond to 
# sites views. The first list is the site visited, the second is
# the user who visited the site.

# See the test cases for more details.

from pprint import pprint

debug   = 0
verbose = 0
# flag var to add '\n' after certain '\r' operations
globalVar = {'terminateCarriageReturn' : 0,}

'''
For any pair of pages (P,Q) define the affinity to be the number of persons who viewed both.

Your goal in this lab is to take as input log file data and return the pair of pages that has the highest affinity. In case of ties return any maximum common count pair. See the provided template code for details.
'''
'''
Steps

Read through the test cases, make sure you understand the expected results. You can run the test cases as python programs, i.e., python test1.py. (All files must be in the same directory.) 
If your solution is incorrect, you will see an assertion failure. 
If it passes, the test does not print anything.
Submit your finished compute_highest_affinity.py source code file via blackboard.
'''
################################################################

def collate_data(site_list, user_list, time_list):
  printInfo("begin reading in site data")
  # 1. Check that input data is sane
  #  i.e. all lists are same length
  # 2. Populate a dict with data per website
  # webLogDict[site][user][[time]]
  # dict for sites
  #   dict for users
  #     list for times

  # hold message and return value
  retStr = ""
  retVal = 1

  webLogDict = {}
  # check that all three lists are same length
  if(len(site_list) != len(user_list) != len(time_list)):
    retStr = "input list mismatch."
    retVal = 1
  else:
    # loop through all three lists and populate the webLogDict
    for index in range(0,len(site_list)):
      tmpSite = site_list[index]
      tmpUser = user_list[index]
      tmpTime = time_list[index]
      # define key:site as hash if not present
      if (tmpSite not in webLogDict):
        webLogDict[tmpSite] = {}
      # define key:user as array if not present. user-array for timestamps
      if (tmpUser not in webLogDict[tmpSite]):
        webLogDict[tmpSite][tmpUser] = []
      # add timestamp array if not present
      webLogDict[tmpSite][tmpUser].append([tmpTime])
      #else:
        #webLogDict[tmpSite]
  #</assimilate data>

  for siteName in webLogDict:
    webLogDict[siteName]['userSet'] = set(webLogDict[siteName])


  if(verbose >= 3):
    pprint(webLogDict)
  printInfo("end reading in site data")
  return webLogDict
#</def collate_data> 

#<def calculate_affinity>
#TODO: this is a terribly inappropriate function call
def calculate_affinity(siteDataDict, siteP, siteQ):
  affinity = 0
  if(siteP in siteDataDict and siteQ in siteDataDict):
    commonThings = siteDataDict[siteP]['userSet'].intersection(siteDataDict[siteQ]['userSet'])
    affinity = len(commonThings)
  return affinity
#</def calculate_affinity>

#< def printInfo>
def printInfo(printme):
  # if verbosity not defined, set to one
  if(verbose >= 1):
    print("info : " + printme)
   #print("Warn : " + printme)
   #print("ERROR: " + printme)
#</def printInfo>


def highest_affinity(site_list, user_list, time_list):
  # Returned string pair should be ordered by dictionary order
  # I.e., if the highest affinity pair is "foo" and "bar"
  # return ("bar", "foo"). 

  # add data to a dict
  siteDataDict = collate_data(site_list, user_list, time_list)

  # < find most users>
  # find site with most users
  # bug - does not account for multiple users in one list
  numUsers = -1
  for siteName in siteDataDict:
    numUsersTmp = len(siteDataDict[siteName])
    if(numUsersTmp > numUsers):
      numUsers = numUsersTmp
  # </find most users>

  # < calculate affinities>
  # strategy: compare site_n to remaining sites site_n+[1,end] , then site_(n+1) to site_(n+1)+[1,end]
  # track compared sites to avoid situation e.g. 'a intersect b' followed by 'b intersect a'
  visitedSites = []
  affinityList = []
  affinityPairsDict = {}
  affinityDict = {}
  #for currentSite in range(1,len(siteDataDict)):
  for currentSite in siteDataDict:
    printInfo("checking affinity for " + currentSite)
    # skip this site for future comparisson
    visitedSites.append(currentSite)
    # get intersection of userSet for current site and all remaining sites
    siteCounter = 0
    for nextSite in siteDataDict:
      siteCounter += 1
      # do not compare to visited sites (including self)
      if nextSite in visitedSites:
        if(debug >= 2):
          #print("skipping " + nextSite + " while comparing to " + currentSite)
          print("skipping " + nextSite)# + " while comparing to " + currentSite)
        continue
      #printInfo("  comparing to " + currentSite)
      import sys
      if(verbose >= 1):
        globalVar['terminateCarriageReturn'] = 1
        sys.stdout.write("\r" + str(siteCounter) + "  comparing to " + nextSite)
      #ver1 this would be pair = affinity
      affinityPairsDict[(currentSite,nextSite)] = \
      calculate_affinity(siteDataDict,currentSite,nextSite)
      #ver2 this would be affinity = pair
      #TODO: dict key affinity, value array of tuples to track multiple equal affinities
      affinityDict[ calculate_affinity(siteDataDict,currentSite,nextSite)] = \
          (currentSite,nextSite)
    # </'for nextSite in siteDataDict:'>
    if(globalVar['terminateCarriageReturn'] == 1): # tied to the sys.stdout.write("\r") a few lines above
      print("")
    #siteDataDict[currentSite]['userSet']
    #for remainingSite in range(currentSite+1,len(siteDataDict)):
  # </calculate affinities>

  # < find highest affinity>
  # https://docs.python.org/2/library/functions.html#max
  # 'sorted' returns a list, so cast/convert to tuple
  maxAffinityTuple = tuple(\
      sorted(\
        affinityDict[(max(affinityDict))]
        )
      )







  return maxAffinityTuple
  return ('abc', 'def')
#</def highest_affinity> 

