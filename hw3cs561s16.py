#@author: Sagar Bharat Makwana
#Last Updated at 00:34 PST on 04/12/2016

import copy
#-----------------------------------Function and Definitions------------------------------

#Splits the given literal into its variable and the value(eg. LeakIdea = +)
def splitLiteral(literal):
    literal = literal.strip()
    holder = literal.split(' = ')
    variable = holder[0].strip()
    value = holder[1].strip()
    value = True if value == '+' else False
    return variable,value

#Sorts the nodes in the topological order and returns the topological sorted list of nodes
def topologicalSort(bayesnet):
    nodes = bayesnet.keys()
    sortedNodes = []

    while len(sortedNodes) < len(nodes):
        for node in nodes:
            if node not in sortedNodes and all(parent in sortedNodes for parent in bayesnet[node]['parents']):
                sortedNodes.append(node)

    return sortedNodes

#Returns only the node that are required for the query.
def nodeSelection(evidence,bayesnet,sortedNodes):
    addedNodeSet = set(evidence.keys())
    isNodePresent = [True if x in addedNodeSet else False for x in sortedNodes]

    while len(addedNodeSet) != 0:
        popNode = addedNodeSet.pop()
        for parent in bayesnet[popNode]['parents']:
            addedNodeSet.add(parent)
            parentIndex = sortedNodes.index(parent)
            isNodePresent[parentIndex] = True

    newSortedNodes = []
    for node in sortedNodes:
        if isNodePresent[sortedNodes.index(node)] == True:
            newSortedNodes.append(node)

    return newSortedNodes

def enumeration(vars,e):
    if len(vars) == 0:
        return 1.0

    Y = vars[0]

    if Y in e:
        result = probability(Y,e)*enumeration(vars[1:],e)
    else:
        sumProbability = []
        e2 = copy.deepcopy(e)
        for y in [True,False]:
            e2[Y] = y
            sumProbability.append(probability(Y,e2)*enumeration(vars[1:],e2))
        result =sum(sumProbability)

    return result

#TODO: Implementation to be done
def probability(Y,e):
    print Y


#-----------------------------------Input-------------------------------------------------

#Bayesian Network Dictionary
BayesNet = {}
rawQueryList = []
#Reading the input file

#filename = sys.argv[-1]
filename = 'input.txt'
inputFile = open(filename)

#Building queries from input
line = inputFile.readline().strip()
while line != '******':
    rawQueryList.append(line)
    line = inputFile.readline().strip()

#Building the bayesian network from input
line = ' '
while line != '':
    #Declaring the parent list
    parents = []
    # Input the node names and the parents
    line = inputFile.readline().strip()

    nodeAndParents = lines = line.split(' | ')
    node = nodeAndParents[0].strip()

    if len(nodeAndParents) != 1:
        parents = nodeAndParents[1].strip().split(' ')

    BayesNet[node] = {}
    BayesNet[node]['parents'] = parents
    BayesNet[node]['children']=[]

    #Insert child for all the parents
    for parent in parents:
        BayesNet[parent]['children'].append(node)

    # Input the probabilities

    if len(parents) == 0:
        line = inputFile.readline().strip()
        if line == 'decision':
            #Decision Node
            BayesNet[node]['type'] = 'decision'
        else:
            #Node with prior probability
            BayesNet[node]['type'] = 'normal'
            BayesNet[node]['prob'] = line
    else:
        #Nodes with conditional probabilies
        condprob = {}
        for i in range(0,pow(2,len(parents))):
            line = inputFile.readline().strip()
            lines = line.split(' ')
            prob = lines[0]
            lines = lines[1:]
            truth = tuple(True if x == '+' else False for x in lines)
            condprob[truth] = prob

        BayesNet[node]['type'] = 'normal'
        BayesNet[node]['condprob'] = condprob

    line = inputFile.readline().strip()

#--------------------------------Query Inferencing---------------------------------------------

sortedNodes = topologicalSort(BayesNet)
#Query Inferencing for all the input queries

for query in rawQueryList:

    evidence = {}
    operation = query[:query.index('(')]
    operation = operation.strip()

    if operation == 'P':
        print 'Operation P'
        literals = query[query.index('(')+1:query.index(')')]
        orIndex = literals.index('|') if '|' in literals else -1
        #If both query and evidence is given.
        if orIndex != -1:
            holder = literals[:literals.index(' | ')]
            xVar,xVal = splitLiteral(holder)
            evidence[xVar] = xVal
            holder = literals[literals.index(' | ')+3:]
        #If only evidence is given
        else:
            holder  = literals

        literals = holder.strip()
        literals = literals.split(',')
        for literal in literals:
            var,val = splitLiteral(literal)
            evidence[var] = val

        sortedNodesForQuery = nodeSelection(evidence,BayesNet,sortedNodes)

    elif operation == 'EU':
        print 'Operation EU'
    else:
        print 'Operation MEU'





