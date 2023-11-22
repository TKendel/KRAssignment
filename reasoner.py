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
        self.updated = True
        self.positionSaver = None
        self.graph = {}
        self.key_index = 0
        self.concept = None
        self.node = None

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
        self.graph["d0"] = []
        while self.updated:
            print(self.updated)
            self.updated = False
            print("New turn")
            self.print_java_object_dict(self.reasonerDict)
            new_node_to_dict = False
            for key, item in self.reasonerDict.items(): # key means node here, like d0
                for index, concept in enumerate(item):  # item is the list of concepts like ['(A ⊓ B)', 'A', 'B']
                    self.print_java_object_list(item)
                    print("fasz")
                    print(len(item))
                    conceptDictType = concept.getClass().getSimpleName()
                    print(f"Item: {formatter.format(concept)}; Type: {conceptDictType}")

                    if conceptDictType == "ConceptConjunction":
                        self.updated = self.conjunctionRule(concept, key)
                    if conceptDictType == "ExistentialRoleRestriction":
                        new_node_to_dict = self.existenceRuleOne(concept, key)
                    if new_node_to_dict:
                        break

            if new_node_to_dict:
                self.reasonerDict[f"d{self.key_index}"] = [self.concept.filler()]
                self.graph[self.node].append((self.concept.role(), f"d{self.key_index}"))
                self.updated = True
        
        self.print_java_object_dict(self.reasonerDict)
        


reasoner = Reasoner("pizza.owl")

elFactory = gateway.getELFactory()
# subsume = elFactory.getConceptName('"CowAndWow"')

conceptA = elFactory.getConceptName("A")
r = elFactory.getRole("r")
t = elFactory.getRole("t")
conceptB = elFactory.getConceptName("B")
exist_r_B = elFactory.getExistentialRoleRestriction(r, conceptB)
conceptC = elFactory.getConceptName("C")
conceptD = elFactory.getConceptName("D")
conjunctionAB = elFactory.getConjunction(conceptA, conceptB)
conjunctionAD = elFactory.getConjunction(conceptA, conceptD)
conjunctionCD = elFactory.getConjunction(conceptC, conceptD)
conjunctionABAD = elFactory.getConjunction(conjunctionAB, conjunctionAD)
conjunctionArB = elFactory.getConjunction(conceptA, exist_r_B)
reasoner.getSubsumers(conjunctionArB)

# reasoner = Reasoner(sys.argv[1])
# reasoner.getSubsumers(sys.argv[2])