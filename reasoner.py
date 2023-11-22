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
        self.nodeCounter = 0
        self.routingTable = {}
        self.subsumer = 0
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
        axioms = self.parseOntologyTBox()
        self.reasonerDict["d0"].append(subsume)
        for concept in allConcepts:
            print(self.reasonerDict)
            self.graph["d0"] = []
            while self.updated:
                print(self.updated)
                self.updated = False
                print("New turn")
                self.print_java_object_dict(self.reasonerDict)
                new_node_to_dict = False
                for key in list(self.reasonerDict): # key means node here, like d0
                    for index, conceptDict in enumerate(self.reasonerDict[key]):  # item is the list of concepts like ['(A ⊓ B)', 'A', 'B']
                        if concept in self.reasonerDict["d0"]:
                            self.subsumer += 1
                        else:
                            self.print_java_object_list(self.reasonerDict[key])
                            print("fasz")
                            print(len(self.reasonerDict[key]))
                            conceptDictType = conceptDict.getClass().getSimpleName()
                            print(f"Item: {formatter.format(conceptDict)}; Type: {conceptDictType}")

                            if conceptDictType == "ConceptConjunction":
                                self.updated = self.conjunctionRule(conceptDict, key)
                            if conceptDictType == "ExistentialRoleRestriction":
                                self.existenceRuleOnePointTwo(conceptDict, key)
                            self.existenceRuleTwo()

                # if new_node_to_dict:
                #     self.reasonerDict[f"d{self.key_index}"] = [self.concept.filler()]
                #     self.graph[self.node].append((self.concept.role(), f"d{self.key_index}"))
                #     self.updated = True

            self.print_java_object_dict(self.reasonerDict)
            print(self.graph)

                # for axiom in axioms:
                #     for individual in self.reasonerDict.keys():
                #         conceptDictList = self.reasonerDict[individual]
                #         for conceptDict in conceptDictList:
                #             print(conceptDict)
                #             strConcept = formatter.format(conceptDict)
                #             strAxiom = formatter.format(axiom)
                #             if formatter.format(conceptDict) not in formatter.format(axiom):
                #                 continue
                #             else:
                #                 lhsAxiom = formatter.format(axiom.lhs())
                #                 rhsAxiom = formatter.format(axiom.rhs())
                #                 # Add boht the left and right side into the d array 
                #                 self.reasonerDict[individual].append(lhsAxiom)
                #                 self.reasonerDict[individual].append(rhsAxiom)
                #                 self.updated = True
                #                 break


reasoner = Reasoner("pizza.owl")

elFactory = gateway.getELFactory()
subsume = elFactory.getConceptName('"Margherita"')

conceptA = elFactory.getConceptName("A")
r = elFactory.getRole("r")
t = elFactory.getRole("t")
conceptB = elFactory.getConceptName("B")
exist_r_B = elFactory.getExistentialRoleRestriction(r, conceptB)
conceptC = elFactory.getConceptName("C")
conceptD = elFactory.getConceptName("D")
conjunctionAB = elFactory.getConjunction(conceptA, conceptB)
role = elFactory.getRole("r")
existential = elFactory.getExistentialRoleRestriction(role,conjunctionAB)
reasoner.getSubsumers(existential)

# reasoner = Reasoner(sys.argv[1])
# reasoner.getSubsumers(sys.argv[2])