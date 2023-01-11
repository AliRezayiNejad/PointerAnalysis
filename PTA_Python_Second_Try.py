# No v.pointsTo overwrites, Not dependant on statement order

import json

filePath = input('Please enter the full path to your JSON file: ')
with open(filePath, 'r') as file:
    userInput = json.load(file)


class variable:
  def __init__(self, name):
      self.name = name
      self.pointsTo = None
  def __repr__(self):
      return "{{ \"location\": \"{0}\", \"ptset\": [{1}]}}".format(self.name, self.pointsTo)

variablesFromNew = []
variablesFromAssign = []
variablesFromFW = []
variablesFromFR = []

for i in range(len(userInput)):

    if userInput[i]["type"]=="new":
        v = variable(userInput[i]["lhs"])
        v.pointsTo = userInput[i]["rhs"]
        variablesFromNew.append(v)


for i in range(len(userInput)):

    if userInput[i]["type"]=="assign":
        for anyVar in variablesFromNew:
            if anyVar.name == userInput[i]["rhs"]:
                v = variable(userInput[i]["lhs"])
                v.pointsTo = anyVar.pointsTo
                variablesFromAssign.append(v) #y->B is added
                for anyV in variablesFromAssign:
                    for statement in userInput:
                        if statement["type"] == "assign":
                            if statement["rhs"] == anyV.name:
                                v = variable(statement["lhs"])
                                v.pointsTo = anyV.pointsTo
                                variablesFromAssign.append(v)
    

variablesNewAssign = variablesFromNew + variablesFromAssign

for i in range(len(userInput)):

    if userInput[i]["type"]=="fieldwrite":
        v = variable(userInput[i]["lhs"])
        for letter in userInput[i]["lhs"]:
            for h in range(len(variablesNewAssign)):
                if variablesNewAssign[h].name == letter:
                    v = variable(userInput[i]["lhs"].replace(letter, variablesNewAssign[h].pointsTo))
                if variablesNewAssign[h].name == userInput[i]["rhs"]:
                    v.pointsTo = variablesNewAssign[h].pointsTo
        variablesFromFW.append(v)


variablesNewAssignFW = variablesFromNew + variablesFromAssign + variablesFromFW

for i in range(len(userInput)):
    
    if userInput[i]["type"]=="fieldread":
        v = variable(userInput[i]["lhs"])
        for letter in userInput[i]["rhs"]:
            for h in range(len(variablesNewAssignFW)):
                if letter == variablesNewAssignFW[h].name:
                    v.pointsTo = userInput[i]["rhs"].replace(letter, variablesNewAssignFW[h].pointsTo)
            for g in range(len(variablesNewAssignFW)):
                if variablesNewAssignFW[g].name == v.pointsTo:
                    v.pointsTo = variablesNewAssignFW[g].pointsTo
        variablesFromFR.append(v)

    #else:
        #print("Operation type must be one of the following: new, assign, fieldwrite, fieldread.")


variables = variablesFromNew + variablesFromAssign + variablesFromFW + variablesFromFR
print()
#print(variablesFromNew)
#print(variablesFromAssign)
#print(variablesFromFW)
#print(variablesFromFR)
print(variables)

