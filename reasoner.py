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
        self.subsumer = 0
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
        axioms = self.parseOntologyTBox()
        self.reasonerDict["d0"].append(subsume)
        for concept in allConcepts:
            '''
            Right now for each concept that we are checking we are also dismantling the provided concept / our subsume.
            This can be done better but for now lets keep it like this unless you have a better solution
            My brain is not working as you saw with the conjuntuon rule :)
            '''
            while self.updated:
                self.updated = False
                for individual in self.reasonerDict.keys():
                    conceptDictList = self.reasonerDict[individual]
                    for counter in range(len(conceptDictList)):
                        # To keep track of concepts which were ran through the rules so we dont get stuck in an infinite loop
                        if counter == self.positionSaver:
                            continue
                        elif concept in self.reasonerDict["d0"]:
                            self.subsumer += 1
                        else:
                            conceptDictType = conceptDictList[counter].getClass().getSimpleName()
                            print()
                            print(self.reasonerDict)
                            if conceptDictType == "ConceptName":
                                break
                            elif conceptDictType == "ConceptConjunction":
                                self.conjunctionRule(conceptDictList[counter], individual)
                                self.updated = True
                                self.updatedKey = individual
                                self.positionSaver = counter
                                break
                            elif conceptDictType == "ExistentialRoleRestriction":
                                pass
                for axiom in axioms:
                    for individual in self.reasonerDict.keys():
                        conceptDictList = self.reasonerDict[individual]
                        for conceptDict in conceptDictList:
                            strConcept = formatter.format(conceptDict)
                            strAxiom = formatter.format(axiom)
                            if formatter.format(conceptDict) not in formatter.format(axiom):
                                continue
                            else:
                                lhsAxiom = formatter.format(axiom.lhs())
                                rhsAxiom = formatter.format(axiom.rhs())
                                # Add boht the left and right side into the d array 
                                self.reasonerDict[individual].append(lhsAxiom)
                                self.reasonerDict[individual].append(rhsAxiom)
                                self.updated = True
                                break

        print(self.reasonerDict)
        


reasoner = Reasoner("pizza.owl")

elFactory = gateway.getELFactory()
subsume = elFactory.getConceptName('"Margherita"')

conceptA = elFactory.getConceptName("A")
conceptB = elFactory.getConceptName("B")
conjunctionAB = elFactory.getConjunction(conceptA, conceptB)
reasoner.getSubsumers(subsume)

# reasoner = Reasoner(sys.argv[1])
# reasoner.getSubsumers(sys.argv[2])