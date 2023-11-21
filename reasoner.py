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

def print_java_object_dict(dictionary):
    to_print = dict(map(lambda x : (x[0], list(map(lambda object : formatter.format(object), x[1]))), dictionary.items()))
    print(to_print)
    return to_print

def print_java_object_list(object_list):
    to_print = list(map(lambda object : formatter.format(object), object_list))
    print(to_print)
    return to_print

class Reasoner(CompletionRulesApplication):
    def __init__(self, ontology) -> None:
        self.ontology = parser.parseFile(ontology)
        self.reasonerDict = {"d0": []}
        self.updated = True
        self.positionSaver = None
        self.updatedKey = None

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
        while self.updated:
            self.updated = False
            # print_java_object_dict(self.reasonerDict)
            for key, item in self.reasonerDict.items(): # key means node here, like d0
                for index, concept in enumerate(item):  # item is the list of concepts like ['(A ⊓ B)', 'A', 'B']
                    # print_java_object_list(item)
                    # To keep track of concepts which were ran through the rules so we dont get stuck in an infinite loop
                    if index == self.positionSaver:
                        continue
                    else:
                        conceptDictType = concept.getClass().getSimpleName()
                        # print(conceptDictType)
                        # concept.getConjuncts()
                        # print_java_object_dict(self.reasonerDict)
                        # self.conjunctionRuleTwo(concept, key)
                        if conceptDictType == "ConceptName":
                            break
                        if conceptDictType == "ConceptConjunction":
                            self.conjunctionRule(concept, key)
                            self.updated = True
                            self.updatedKey = key
                            self.positionSaver = index
                            break
                        if conceptDictType == "ExistentialRoleRestriction":
                            pass
        
        print(self.reasonerDict)
        


reasoner = Reasoner("pizza.owl")

elFactory = gateway.getELFactory()
subsume = elFactory.getConceptName('"CowAndWow"')

conceptA = elFactory.getConceptName("A")
conceptB = elFactory.getConceptName("B")
conjunctionAB = elFactory.getConjunction(conceptA, conceptB)
reasoner.getSubsumers(conjunctionAB)

# reasoner = Reasoner(sys.argv[1])
# reasoner.getSubsumers(sys.argv[2])