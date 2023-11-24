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

ELConcepts = ["UniversalRoleRestriction", "ConceptDisjunction", "ConceptComplement", "DisjointnessAxiom"]
axiomBanedList = ["DomainAxiom", "DisjointnessAxiom", "RangeAxiom"]

class Reasoner(CompletionRulesApplication):
    def __init__(self, ontology) -> None:
        self.ontology = parser.parseFile(ontology)
        self.reasonerDict = None
        self.nodeCounter = 0
        self.routingTable = {}
        self.subsumer = 0
        self.updated = True
        self.positionSaver = None
        self.graph = {}
        self.key_index = 0
        self.concept = None
        self.node = None
        self.elFactory = gateway.getELFactory()

    def parseOntologyTBox(self):
        axiomList = []
        tbox = self.ontology.tbox()
        axioms = tbox.getAxioms()
        for axiom in axioms:
            if axiom.getClass().getSimpleName() not in axiomBanedList:
                axiomList.append(axiom)
        return axiomList


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
        for concept in allConcepts:
            # print(self.reasonerDict)
            self.reasonerDict = {"d0": []}
            self.reasonerDict["d0"].append(subsume)
            self.graph["d0"] = []
            while self.updated:
                # print(self.updated)
                self.updated = False
                # print("New turn")
                # self.print_java_object_dict(self.reasonerDict)
                new_node_to_dict = False
                for key in list(self.reasonerDict): # key means node here, like d0
                    for index, conceptDict in enumerate(self.reasonerDict[key]):  # item is the list of concepts like ['(A ⊓ B)', 'A', 'B']
                        if concept in self.reasonerDict["d0"]:
                            self.subsumer += 1
                            break
                        else:
                            # self.print_java_object_list(self.reasonerDict[key])
                            # print("fasz")
                            # print(len(self.reasonerDict[key]))
                            conceptDictType = conceptDict.getClass().getSimpleName()
                            # print(f"Item: {formatter.format(conceptDict)}; Type: {conceptDictType}")
                            # if conceptDictType == "ConceptName":
                            #     self.conjunctionRuleTwo(conceptDict, key)
                            if conceptDictType == "ConceptConjunction":
                                self.updated = self.conjunctionRule(conceptDict, key)
                            if conceptDictType == "ExistentialRoleRestriction":
                                self.existenceRuleOnePointTwo(conceptDict, key)
                            self.existenceRuleTwo()

                # if new_node_to_dict:
                #     self.reasonerDict[f"d{self.key_index}"] = [self.concept.filler()]
                #     self.graph[self.node].append((self.concept.role(), f"d{self.key_index}"))
                #     self.updated = True

                for axiom in axioms:
                    axiomType = axiom.getClass().getSimpleName()
                    # print(axiom)
                    # print(formatter.format(axiom))
                    if axiomType == "EquivalenceAxiom":
                        conceptsInEquivalence = []
                        for concept in axiom.getConcepts():
                            conceptsInEquivalence.append(concept)
                        newGCIfirst = self.elFactory.getGCI(conceptsInEquivalence[0], conceptsInEquivalence[1])
                        newGCIsecond = self.elFactory.getGCI(conceptsInEquivalence[1], conceptsInEquivalence[0])
                        for individual, conceptList in self.reasonerDict.items():
                            for conceptInList in conceptList:
                                if newGCIfirst.lhs() == conceptInList and newGCIfirst.rhs() not in conceptList:
                                    # Add right side
                                    self.reasonerDict[individual].append(newGCIfirst.rhs())
                                    self.updated = True
                                    break
                                if newGCIsecond.lhs() == conceptInList and newGCIsecond.rhs() not in conceptList:
                                    # Add right side
                                    self.reasonerDict[individual].append(newGCIsecond.rhs())
                                    self.updated = True
                                    break
                    else:
                        lhsAxiom = axiom.lhs()
                        for individual, conceptList in self.reasonerDict.items():
                            for conceptInList in conceptList:
                                if lhsAxiom == conceptInList and axiom.rhs() not in conceptList:
                                    # Add boht the left and right side into the d array 
                                    self.reasonerDict[individual].append(axiom.rhs())
                                    self.updated = True
                                    break
                self.print_java_object_dict(self.reasonerDict)
            print(self.subsumer)


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
reasoner.getSubsumers(subsume)

# reasoner = Reasoner(sys.argv[1])
# reasoner.getSubsumers(sys.argv[2])