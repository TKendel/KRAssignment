import sys
from completionRulesApplication import CompletionRulesApplication
#! /usr/bin/python

from py4j.java_gateway import JavaGateway

# connect to the java gateway of dl4python
gateway = JavaGateway()

# get a parser from OWL files to DL ontologies
parser = gateway.getOWLParser()

# get a formatter to print in nice DL format
formatter = gateway.getSimpleDLFormatter()

class Reasoner(CompletionRulesApplication):
    def __init__(self, ontology) -> None:
        self.onotology = ontology
        self.reasonerDict = {"d0": None}

    def parseOntology(self):
        return self.ontology.tbox()

    def getSubsumers(self, subsumed):
        self.reasonerDict["d0"] = subsumed
        updated = True
        for concept in self.reasonerDict.keys():
            self.ruleApplication(self.reasonerDict[concept])
        


reasoner = Reasoner("pizza.owl")
reasoner.getSubsumers("CowAndWow")

# reasoner = Reasoner(sys.argv[1])
# reasoner.getSubsumers(sys.argv[2])