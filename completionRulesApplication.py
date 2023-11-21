from py4j.java_gateway import JavaGateway

# connect to the java gateway of dl4python
gateway = JavaGateway()

# get a parser from OWL files to DL ontologies
parser = gateway.getOWLParser()

# get a formatter to print in nice DL format
formatter = gateway.getSimpleDLFormatter()

class CompletionRulesApplication:
    def __init__(self) -> None:
        self.tBox = None
        self.concept = None

    def searchAxioms(self):
        pass

    # I dont think this is needed since we are doing a checkup for the concept at the start when providing a subsume
    def getConcept(self, conceptDict):
        # Probably dont need these messages but i kept it for debugging purposes
        if conceptDict not in self.tBox:
            print(f"The concept {conceptDict} does not exist!")
        else:
            print(f"Concept {conceptDict} exists")

    def conjunctionRule(self, conceptDict, individual):
        for conjunct in conceptDict.getConjuncts():
            if conjunct not in self.reasonerDict.values():
                self.reasonerDict[individual].append(conjunct)

    def conjunctionRuleTwo(self):
        pass

    def existenceRuleOne(self):
        pass

    def existenceRuleTwo(self):
        pass

    # def ruleApplication(self, reasonerDict, concept, tBox):
    #     self.reasonerDict = reasonerDict
    #     self.tBox = tBox
    #     self.concept = concept
    #     self.updated = True
    #     self.
    #     while self.updated:
    #         self.updated = False
    #         for individual in reasonerDict.keys():
    #             conceptDictList = reasonerDict[individual]
    #             for conceptDict in conceptDictList:
    #                 conceptDictType = conceptDict.getClass().getSimpleName()
    #                 print()
    #                 print(self.reasonerDict)
    #                 if conceptDictType == "ConceptName":
    #                     break
    #                 if conceptDictType == "ConceptConjunction":
    #                     self.conjunctionRule(conceptDict, individual)
    #                     self.updated = True
    #                     break
    #                 if conceptDictType == "ExistentialRoleRestriction":
    #                     pass