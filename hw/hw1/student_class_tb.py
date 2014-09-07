from pprint import pprint
import random
from ipdb import *
import copy

# turn on breakpoints
pdebug = 0


from student_class import Student

def genRandomStudent(**kwargs):
  _seed = random.random()
  if(kwargs):
    _seed = kwargs['seed']
  nameRand = str(random.random())
  # 400 * 0.393 = 157.2 ; int(157.2) = 157 ; float(157 / 100)
  gpaRand = float( int(400 * random.random() ) * 0.01)
  ageRand = int(100 * random.random())

  # use the generated seed
  nameRand = str(_seed)
  gpaRand = float( int(400 * _seed ) * 0.01)
  ageRand = int(100 * _seed) % 100 # not sure if the modulo is a bad idea
  ageRand = int(100 * _seed)
  return Student(nameRand,gpaRand,ageRand)
  
#def printSeparator(**kwargs):
def printSeparator(*args,**kwargs):
  width = 30 
  if(kwargs):
    if(kwargs['width']):
      width = kwargs['width']
  if(args):
    width = args[0]
  print("#" * width)
  return

student1 = Student('Zacharias',3.8,20)
print("#" * 30)
print("-I-: checking student class:")
print("  checking __str__ function")
print(type(student1.__str__()))
print(student1.__str__())
print("  checking __str__ function")
print(type(student1.__hash__()))
print(student1.__hash__())
print("#" * 30)

printSeparator()
# create new student
student2 = genRandomStudent(seed=4)
# create equal student
student3 = copy.deepcopy(student2)
# create less student
student4 = genRandomStudent(seed=3)
#student2 = genRandomStudent()
# https://docs.python.org/2/reference/datamodel.html#object.__lt__
print("-I-: comparison tests:")
print("     equality check:")
print("is student A == student B?:")
print("student A: " + student2.__str__())
print("student B: " + student3.__str__())
if(student2.__eq__(student3)):
  print("-I-: PASS")
else:
  print("-E-: FAIL")
  print(student2 + student3)
print("     lesser-than check:")
print("is student C < student A?:")
print("student A: " + student2.__str__())
print("student C: " + student4.__str__())
if(student4.__lt__(student2) and (student4 < student2)):
  print("-I-: PASS")
else:
  print("-E-: FAIL")
printSeparator()
### check sorted()
print("-I-: test list sort:")
if(pdebug == 1):
  set_trace()

# generate list of student-objects with random attributes
studentList = [genRandomStudent() for rand in xrange(10)]
print("    random list :")
print(">>> studentList = [genRandomStudent() for rand in xrange(10)] ")
print("")
for x in (studentList):
  print(x)
del x
print("  sorted list :")
print(">>> for x in sorted(studentList): print(x)")
for x in sorted(studentList):
  print(x)

printSeparator()
if(pdebug == 1):
  set_trace()
### check dict()
print("-I-: test dict sort:")
print("     random dict:")
print(">>> studentDict = {genRandomStudent():1 for i in range(10)}")
print("")

# generate dict of student-objects with random attributes
studentDict = {genRandomStudent():1 for i in range(10)}
for x in (studentDict):
  print(x)
print("    sorted dict:")
print(">>> for x in sorted(studentDict): print(x)")
for x in sorted(studentDict):
  print(x)
if(pdebug == 1):
  set_trace()
printSeparator()
studentList = []
for num in range(0,2):
  print(num)
  studentList.append(genRandomStudent())

print
