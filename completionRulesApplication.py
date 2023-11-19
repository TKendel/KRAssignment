from py4j.java_gateway import JavaGateway

# connect to the java gateway of dl4python
gateway = JavaGateway()

# get a parser from OWL files to DL ontologies
parser = gateway.getOWLParser()

# get a formatter to print in nice DL format
formatter = gateway.getSimpleDLFormatter()



# load an ontology from a file
ontology = parser.parseFile("pizza.owl")

print("Loaded the ontology!")

# IMPORTANT: the algorithm from the lecture assumes conjunctions to always be over two concepts
# Ontologies in OWL can however have conjunctions over an arbitrary number of concpets.
# The following command changes all conjunctions so that they have at most two conjuncts
print("Converting to binary conjunctions")
gateway.convertToBinaryConjunctions(ontology)

# get the TBox axioms
tbox = ontology.tbox()
axioms = tbox.getAxioms()

# Creating EL concepts and axioms


elFactory = gateway.getELFactory()

conceptA = elFactory.getConceptName("A")
conceptB = elFactory.getConceptName("B")
conjunctionAB = elFactory.getConjunction(conceptA, conceptB)
role = elFactory.getRole("r")
existential = elFactory.getExistentialRoleRestriction(role,conjunctionAB)
top = elFactory.getTop()
conjunction2 = elFactory.getConjunction(top,existential)

gci = elFactory.getGCI(conjunctionAB,conjunction2)
print((formatter.format(gci)))

elFactory = gateway.getELFactory()

conceptA = elFactory.getConceptName("A")
conceptB = elFactory.getConceptName("B")
conjunctionAB = elFactory.getConjunction(conceptA, conceptB)
test = {"d0": [formatter.format(conjunctionAB)]}

list = []
for axiom in axioms:
    list.append(formatter.format(axiom))

class CompletionRulesApplication:
    def __init__(self, individual, concept, tBox) -> None:
        self.individual = individual
        self.concept = concept
        self.tBox = tBox
        self.ruleApplication()

    def getConcept(self):
        if self.concept in self.tBox:
            print(f"Found the concept {self.concept}")

    def conjunctionRule(self):
        print(self.concept)
        for conjunct in self.concept.getConjuncts():
            print(" - "+formatter.format(conjunct))
            if conjunct not in test.values():
                test[self.individual].append(formatter.format(conjunct))
            elif conjunct not in test.values():
                test[self.individual].append(formatter.format(conjunct))

    def conjunctionRuleTwo(self):
        pass

    def existenceRuleOne(self):
        pass

    def existenceRuleTwo(self):
        pass

    def ruleApplication(self):
        conceptType = self.concept.getClass().getSimpleName()
        if conceptType == "ConceptName":
            self.getConcept()
        elif conceptType == "ConceptConjunction":
            self.conjunctionRule()
        print(test)




test = CompletionRulesApplication("d0", conjunctionAB, list)