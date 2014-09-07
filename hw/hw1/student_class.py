from ipdb import *

#[4] Define a student class in Python. 
# The class should include name, GPA and age fields. 
# Implement__ str__(),  __lt__(), __eq__(), and __hash__() methods.
# Write test code that exercises these methods using sorted() and dict().

#TODO:
#https://docs.python.org/2/library/functools.html#functools.total_ordering
#@total_ordering
class Student:
  def __init__(self,name,gpa,age):
 #   set_trace()
    self.name = name
    self.gpa  = gpa
    self.age  = age

  def __getitem__(self,key):
    return self[key]

  #TODO: research @classmethod
  def __str__(self):
    strValue = "name: " + self.name + " gpa: " + str(self.gpa) + " age: " + str(self.age)
    return strValue

  # https://docs.python.org/2/reference/datamodel.html#object.__repr__
  # TODO: this should look like a valid Python expression that could be used to recreate an object with the same value
  # this seems to allow typing of the instantiation without args
  def __repr__(self):
    strValue = "name: " + self.name + " gpa: " + str(self.gpa) + " age: " + str(self.age)
    return strValue

  # http://stackoverflow.com/a/2909119
  # http://stackoverflow.com/questions/4005318/how-to-implement-a-good-hash-function-in-python
  #   http://stackoverflow.com/a/4005376
  def __hash__(self):
    return 0

  # equals
  def __eq__(self,other):
    retVal = 0 # default 0 for not equal
    #if(self.__compare__(self,other) == [0,0,0]):
    if(self.__compare__(other) == [0,0,0]):
      retVal = 1
    return retVal

  # lesser
  def __lt__(self,other):
    retVal = 0 # default 0 for not lesser-than
    if(self.__compare__(other) == [-1,-1,-1]):
      retVal = 1
    return retVal

  def __compare__(self,other):
    # array where 0:self 1:gpa 2:age
    # set to +1 for other bigger, -1 for other smaller, 0 for equal
    equality = [1,1,1]
    # check name
    if(self.name <= other.name):
      equality[0] -= 1
      if(self.name < other.name):
        equality[0] -= 1
    # check gpa
    if(self.gpa <= other.gpa):
      equality[1] -= 1
      if(self.gpa < other.gpa):
        equality[1] -= 1
    # check age
    if(self.age <= other.age):
      equality[2] -= 1
      if(self.age < other.age):
        equality[2] -= 1
    return equality




