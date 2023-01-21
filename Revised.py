import json

filePath = input('Please enter the full path to your JSON file: ')
with open(filePath, 'r') as file:
    userInput = json.load(file)

class allocationSiteNode:
    def __init__(self, name):
        self.name = name
        self.pointsTo = {} #Key (string) is for the label of the edge(s), value (list) is for allocation site node(s) the arrow(s) points to.
    def __repr__(self):
        return self.name

class variableNode:
    def __init__(self, name):
        self.name = name
        self.pointsTo = set()
    def __repr__(self):
        return "\n{{ \"location\": \"{0}\", \"ptset\": {1}}}".format(self.name, self.pointsTo)

variables = []
allocationSites = []

newedVariableNames = []
newedVariables = []
assignedVariableNames = []
assignedVariables = []
FRvariableNames = []

for statement in userInput:
    if statement["type"] == "new":
        aS = allocationSiteNode(statement["rhs"])
        allocationSites.append(aS)
        if statement["lhs"] not in newedVariableNames:
            newedVariableNames.append(statement["lhs"])
            v = variableNode(statement["lhs"])
            v.pointsTo.add(aS)
            newedVariables.append(v)
        else:
            for var in newedVariables:
                if var.name == statement["lhs"]:
                    var.pointsTo.add(aS)


for statement in userInput: # Newed = Newed statements only
    if statement["type"] == "assign":
        if statement["rhs"] in newedVariableNames: #rhs Newed
            if statement["lhs"] in newedVariableNames: #lhs Newed
                for var1 in newedVariables:
                    if var1.name == statement["lhs"]:
                        for var2 in newedVariables:
                            if var2.name == statement["rhs"]:
                                var1.pointsTo.update(var2.pointsTo)
for statement in userInput: # newly assigned and reassigned = Newed statements only
    if statement["type"] == "assign":
        if statement["rhs"] in newedVariableNames: #rhs Newed
            if statement["lhs"] not in newedVariableNames: #lhs Not Newed
                if statement["lhs"] not in assignedVariableNames: #lhs newly assigned (new var name)
                    v = variableNode(statement["lhs"])
                    for var in newedVariables:
                        if var.name == statement["rhs"]:
                            v.pointsTo.update(var.pointsTo)
                            assignedVariables.append(v)
                    assignedVariableNames.append(statement["lhs"])
                else: #lhs reassigned (var name already in use)
                    for var1 in assignedVariables:
                        if var1.name == statement["lhs"]:
                            for var2 in newedVariables:
                                if var2.name == statement["rhs"]:
                                    var1.pointsTo.update(var2.pointsTo)
for statement in userInput: # newly assigned and reassigned = already assigned statements only
    if statement["type"] == "assign":
        if statement["rhs"] in assignedVariableNames: #rhs assigned
            if statement["lhs"] not in newedVariableNames: #lhs Not Newed
                if statement["lhs"] not in assignedVariableNames: #lhs newly assigned (new var name)
                    for anyV in assignedVariables:
                        for s in userInput:
                            if s["type"] == "assign":
                                if s["rhs"] == anyV.name:
                                    v = variableNode(s["lhs"])
                                    v.pointsTo = anyV.pointsTo
                                    assignedVariables.append(v)
                                    assignedVariableNames.append(s["lhs"])
                else: #lhs reassigned (var name already in use)
                    for var1 in assignedVariables:
                        if var1.name == statement["lhs"]:
                            for var2 in assignedVariables:
                                if var2.name == statement["rhs"]:
                                    var1.pointsTo.update(var2.pointsTo)

variables = newedVariables + assignedVariables
variableNames = newedVariableNames + assignedVariableNames

for statement in userInput:
    if statement["type"] == "fieldwrite":
        v2 = statement["rhs"]
        if "." in statement["lhs"]:
            v1 = statement["lhs"].partition(".")[0]
            arrowLabel = statement["lhs"].partition(".")[2]
            for var in variables:
                if var.name == v1:
                    for aS in var.pointsTo:
                        for aS2 in allocationSites:
                            if aS == aS2:
                                for var2 in variables:
                                    if var2.name == v2:
                                        aS2.pointsTo[arrowLabel] = []
                                        for aS3 in var2.pointsTo:
                                            aS2.pointsTo[arrowLabel].append(aS3)
        else:
            v1 = statement["lhs"].partition("[")[0]
            arrowLabel = "[*]"
            for var in variables:
                if var.name == v1:
                    for aS in var.pointsTo:
                        for aS2 in allocationSites:
                            if aS == aS2:
                                for var2 in variables:
                                    if var2.name == v2:
                                        aS2.pointsTo[arrowLabel] = []
                                        for aS3 in var2.pointsTo:
                                            aS2.pointsTo[arrowLabel].append(aS3)
        for var2 in variables:
            if var2.name == statement["rhs"]:
                FWPT = var2.pointsTo
        for letter in statement["lhs"]:
            for var in variables:
                if var.name == letter:
                    for aS in var.pointsTo:
                        v = variableNode(statement["lhs"].replace(letter, aS.name))
                        v.pointsTo = FWPT
                        variables.append(v)

for statement in userInput:
    if statement["type"] == "fieldread":
        if "." in statement["rhs"]:
            v2 = statement["rhs"].partition(".")[0]
            arrowLabel = statement["rhs"].partition(".")[2]
            if statement["lhs"] not in variableNames:
                v = variableNode(statement["lhs"])
                for var in variables:
                    if var.name == v2:
                        for aS in var.pointsTo:
                            for aS2 in allocationSites:
                                if aS.name == aS2.name:
                                    v.pointsTo.update(aS.pointsTo[arrowLabel])
                variables.append(v)
                variableNames.append(statement["lhs"])
                FRvariableNames.append(statement["lhs"])
            else:
                for v in variables:
                    if v.name == statement["lhs"]:
                        for var in variables:
                            if var.name == v2:
                                for aS in var.pointsTo:
                                    v.pointsTo.update(aS.pointsTo[arrowLabel])
        else:
            v2 = statement["rhs"].partition("[")[0]
            arrowLabel = "[*]"
            if statement["lhs"] not in variableNames:
                v = variableNode(statement["lhs"])
                for var in variables:
                    if var.name == v2:
                        for aS in var.pointsTo:
                            for aS2 in allocationSites:
                                if aS.name == aS2.name:
                                    v.pointsTo.update(aS.pointsTo[arrowLabel])
                variables.append(v)
                variableNames.append(statement["lhs"])
                FRvariableNames.append(statement["lhs"])
            else:
                for v in variables:
                    if v.name == statement["lhs"]:
                        for var in variables:
                            if var.name == v2:
                                for aS in var.pointsTo:
                                    v.pointsTo.update(aS.pointsTo[arrowLabel])

for varname in FRvariableNames: #assign = FR
    for statement in userInput:
        if statement["type"] == "assign":
            if statement["rhs"] == varname:
                v = variableNode(statement["lhs"])
                for var in variables:
                    if var.name == varname:
                        v.pointsTo.update(var.pointsTo)
                variables.append(v)
                FRvariableNames.append(statement["lhs"])

print()
print(variables)
