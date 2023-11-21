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

ELConcepts = ["UniversalRoleRestriction", "ConceptDisjunction", "ConceptComplement"]

class Reasoner(CompletionRulesApplication):
    def __init__(self, ontology) -> None:
        self.ontology = parser.parseFile(ontology)
        self.reasonerDict = {"d0": []}

    def parseOntologyTBox(self):
        tbox = self.ontology.tbox()
        return tbox.getAxioms()

    def parseOntologyConcept(self):
        listOfConcepts = []
        allConcepts = self.ontology.getSubConcepts()
        for concept in allConcepts:
            if concept.getClass().getSimpleName() not in ELConcepts:
                listOfConcepts.append(concept)
        return listOfConcepts

    def getSubsumers(self, subsume):
        allConcepts = self.parseOntologyConcept()
        self.reasonerDict["d0"].append(subsume)
        for concept in allConcepts:
            self.ruleApplication(self.reasonerDict, concept, self.parseOntologyTBox())
        


reasoner = Reasoner("pizza.owl")

elFactory = gateway.getELFactory()
subsume = elFactory.getConceptName('"CowAndWow"')
reasoner.getSubsumers(subsume)

# reasoner = Reasoner(sys.argv[1])
# reasoner.getSubsumers(sys.argv[2])