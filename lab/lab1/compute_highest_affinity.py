# No need to process files and manipulate strings - we will
# pass in lists (of equal length) that correspond to 
# sites views. The first list is the site visited, the second is
# the user who visited the site.

# See the test cases for more details.

from pprint import pprint
verbose = 0

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

  if(verbose >= 1):
    pprint(webLogDict)
  return webLogDict
#</def collate_data> 

def highest_affinity(site_list, user_list, time_list):
  # Returned string pair should be ordered by dictionary order
  # I.e., if the highest affinity pair is "foo" and "bar"
  # return ("bar", "foo"). 

  # add data to a dict
  collate_data(site_list, user_list, time_list)

  return ('abc', 'def')


# idea:
# dict with key of site, dict[site].append(user) and then find max len (dict[site})
