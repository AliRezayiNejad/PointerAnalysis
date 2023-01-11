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

variables = []

for i in range(len(userInput)):

    if userInput[i]["type"]=="new":
        v = variable(userInput[i]["lhs"])
        v.pointsTo = userInput[i]["rhs"]
        variables.append(v)
        for h in range(len(variables)): #new
            if variables[h].pointsTo == userInput[i]["lhs"]: #new
                variables[h].pointsTo = userInput[i]["rhs"] #new

    elif userInput[i]["type"]=="assign":
        v = variable(userInput[i]["lhs"])
        v.pointsTo = userInput[i]["rhs"] #new
        for h in range(len(variables)):
            if variables[h].name == userInput[i]["rhs"]:
                v.pointsTo = variables[h].pointsTo
        variables.append(v)
        for h in range(len(variables)): #new
            if variables[h].pointsTo == userInput[i]["lhs"]: #new
                variables[h].pointsTo = userInput[i]["rhs"] #new

    elif userInput[i]["type"]=="fieldwrite":
        v = variable(userInput[i]["lhs"])
        for letter in userInput[i]["lhs"]:
            for h in range(len(variables)):
                if variables[h].name == letter:
                    v = variable(userInput[i]["lhs"].replace(letter, variables[h].pointsTo))
                if variables[h].name == userInput[i]["rhs"]:
                    v.pointsTo = variables[h].pointsTo
        variables.append(v)
        for h in range(len(variables)): #new
            if variables[h].pointsTo == v.name: #new
                variables[h].pointsTo = v.pointsTo #new

    elif userInput[i]["type"]=="fieldread":
        v = variable(userInput[i]["lhs"])
        v.pointsTo = userInput[i]["rhs"]
        for letter in userInput[i]["rhs"]:
            for h in range(len(variables)):
                if letter == variables[h].name:
                    v.pointsTo = userInput[i]["rhs"].replace(letter, variables[h].pointsTo)
            for g in range(len(variables)):
                if variables[g].name == v.pointsTo:
                    v.pointsTo = variables[g].pointsTo
            for statement in userInput: #new
                if statement["lhs"] == userInput[i]["rhs"]: #new
                    statement["lhs"].replace(letter, variables[h].pointsTo) #new
        variables.append(v)

    else:
        print("Operation type must be one of the following: new, assign, fieldwrite, fieldread.")

print()
print(variables)
