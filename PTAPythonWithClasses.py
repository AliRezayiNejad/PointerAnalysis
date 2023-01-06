#The JSON format for out input just happens to fit very well with how Python implements lists and dictionaries. We can view each item in our input statements as a key:value pair, similar to a dictionary. Python being almost the same as written English helps too!

import json #using the json library, Python to the rescue!

filePath = input('Please enter the full path to your JSON file: ') #As an example, filePath can be C:/Users/Ali/Desktop/The Original Task Example Input.json
with open(filePath, 'r') as file: #the 'r' parameter indicates that we only want to read the file.
    userInput = json.load(file) #Now that we have everything loaded in userInput we can get to work.

#I tried about four different approaches; one was using a list of lists, the first index of each insider list was reserved for an abstract object and all subsequent indexes were home to everything that eventually leads to that abstract object. Another was similer but with defining nodes with "next" attributes instead of lists. The third one was without classes and using a lot of dictionaries, lists and temporary variables.
#Defining a simple class that houses the name and the object type of each variable proved to be the most convenient approach.

class variable:
  def __init__(self, name): #variable name is the only necessary field as later on there are instances where we have to leave the pointsTo attribute empty for a bit.
      self.name = name
      self.pointsTo = None
  def __repr__(self): #to simply print each object at the end. Since each object is presented in a list, the __str__ method will not work as expected.
      return "{{ \"location\": \"{0}\", \"ptset\": [{1}]}}".format(self.name, self.pointsTo) #the sample output from the task had an extra "," in the end which doesn't conform to JSON syntax. Since list item are seperated by a comma by default, I am presenting the end result in list format.

variables = [] #declaring the list that will contain all of our output statements.

for i in range(len(userInput)): #iterating through each statement in the input file individually. Unfortunatly, Python does not support Switch blocks. We have to use a lot of "if"s.

    if userInput[i]["type"]=="new": #scenario 1 out of 4
        #Our simplest and most straight-forward honest statement type. left-hand side points to the abstract object in the right-hand side of the statement. We create an instance of the class we defined with this information and add it to our main list.
        v = variable(userInput[i]["lhs"])
        v.pointsTo = userInput[i]["rhs"]
        variables.append(v)

    elif userInput[i]["type"]=="assign": #scenario 2 out of 4
        #A little more complicated, rhs needs to be evaluated to the object type it eventually refers to.
        v = variable(userInput[i]["lhs"])
        for h in range(len(variables)): #going through all variables added so far.
            if variables[h].name == userInput[i]["rhs"]: #untill we find the variable on the rhs and what it has an arrow to.
                v.pointsTo = variables[h].pointsTo
        variables.append(v)

    elif userInput[i]["type"]=="fieldwrite": #scenario 3 out of 4
        #Getting tricky
        v = variable(userInput[i]["lhs"])
        for letter in userInput[i]["lhs"]: #reading the lhs string letter by letter
            for h in range(len(variables)):
                if variables[h].name == letter: #until we find the corresponding variable
                    v = variable(userInput[i]["lhs"].replace(letter, variables[h].pointsTo)) #and replace the variable name with what it refers to. lhs done.
                if variables[h].name == userInput[i]["rhs"]: #finding and evaluating rhs.
                    v.pointsTo = variables[h].pointsTo
        variables.append(v)

    elif userInput[i]["type"]=="fieldread": #scenario 4 out of 4
        v = variable(userInput[i]["lhs"]) #lhs does not need to be tampered with.
        v.pointsTo = userInput[i]["rhs"]
        for letter in userInput[i]["rhs"]: #going through each letter
            for h in range(len(variables)): #and comparing it with variables we already have.
                if letter == variables[h].name:
                    v.pointsTo = userInput[i]["rhs"].replace(letter, variables[h].pointsTo) #evaluating to reveal its true nature!
            for g in range(len(variables)):
                if variables[g].name == v.pointsTo: #finding the correct abstract object we should eventually arrive at.
                    v.pointsTo = variables[g].pointsTo
        variables.append(v)

    else:
        print("Operation type must be one of the following: new, assign, fieldwrite, fieldread.") #Just in case. scenario 5 out of 4 :)

print()
print(variables)
