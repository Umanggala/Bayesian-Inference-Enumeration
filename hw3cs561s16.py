#@author: Sagar Bharat Makwana
#Last Updated at 22:36 PST on 04/10/2016

#-----------------------------------Function and Definitions------------------------------

#-----------------------------------Input-------------------------------------------------

#Bayesian Network Dictionary
BayesNet = {}

#Reading the input file

#filename = sys.argv[-1]
filename = 'input.txt'
inputFile = open(filename)

#Building queries from input
line = inputFile.readline().strip()
while line != '******':
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

print BayesNet['NightDefense']['condprob'][(False,)]