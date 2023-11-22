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
        self.graph = {}
        self.key_index = 0
        self.node = None

    def print_java_object_dict(self, dictionary):
        to_print = dict(map(lambda x : (x[0], list(map(lambda object : formatter.format(object), x[1]))), dictionary.items()))
        print(to_print)
        return to_print

    def print_java_object_list(self, object_list):
        to_print = list(map(lambda object : formatter.format(object), object_list))
        print(to_print)
        return to_print

    def searchAxioms(self):
        pass

    # I dont think this is needed since we are doing a checkup for the concept at the start when providing a subsume
    def getConcept(self, conceptDict):
        # Probably dont need these messages but i kept it for debugging purposes
        if conceptDict not in self.tBox:
            print(f"The concept {conceptDict} does not exist!")
        else:
            print(f"Concept {conceptDict} exists")

    def conjunctionRule(self, concept, node):
        buffer = False
        for conjunct in concept.getConjuncts():
            if conjunct not in self.reasonerDict[node]:
                self.reasonerDict[node].append(conjunct)
                buffer = True
        return buffer
    
    def is_in_concept(self, concept_to_check, node_to_check):
        if concept_to_check.getClass().getSimpleName() == "ConceptConjunction":
            return all(x in self.reasonerDict[node_to_check] for x in concept_to_check.getConjuncts()) 
        return concept_to_check in self.reasonerDict[node_to_check]

    # def conjunctionRuleTwo(self, concept_lhs, node):
    #     temporary = []
    #     for concept_rhs in self.reasonerDict[node]:
    #         if concept_rhs.getClass().getSimpleName() != "ConceptConjunction" and concept_rhs is not concept_lhs:
    #             temporary.append(gateway.getELFactory().getConjunction(concept_lhs, concept_rhs))
    #     self.reasonerDict[node].extend(list(set(temporary) - set(self.reasonerDict[node])))

    def existenceRuleOne(self, concept, current_node):
        role = concept.role()
        filler = concept.filler()
        # print(self.graph)
        for (relation_iter, node_iter) in self.graph[current_node]: # we go through the relations
            if role == relation_iter and self.reasonerDict[node_iter][0] == filler: # if it already exists in an node
                return False # we have nothing to do
        
        self.key_index += 1
        self.concept = concept
        self.node = current_node
        return True
    
    def existenceRuleOnePointTwo(self, concept, current_node):
        role = concept.role()
        filler = concept.filler()
        # Check if a node exists with the first value being the filler, if so apply sub rule one
        for node in list(self.reasonerDict):
            if node != current_node:
                # There is an existing node with the init concept being our filler
                if self.reasonerDict[node][0] == filler:
                    # Save the route like r : [parent_node, child_node]
                    self.routingTable[role] = [current_node, node]
            else:
                # If no node was found create a new one and make filler its init concept
                self.nodeCounter += 1
                newNode = f"d{self.nodeCounter}"
                internal_marks = {newNode: [filler]}
                self.reasonerDict.update(internal_marks)
                self.routingTable[role] = [current_node, newNode]

    def existenceRuleTwo(self):
        elFactory = gateway.getELFactory()
        # Route look up for every node in the dictionray
        for node, concepts in self.reasonerDict.items():
            for route, connectedNodes in self.routingTable.items():
                # If route has on its r : [parent_node, child_node] parent node the current node,
                # means there is a route coming out of the current node
                if connectedNodes[0] == node:
                    print(self.reasonerDict)
                    # Check all concepts inside which are just concept name. NOT SURE IF IT SHOUDL BE JUST CONCEPT NAMES
                    for conceptChildNode in self.reasonerDict[connectedNodes[1]]:
                        conceptChildNodeType = conceptChildNode.getClass().getSimpleName()
                        if conceptChildNodeType == 'ConceptName':
                            existentialConcept = elFactory.getExistentialRoleRestriction(route, conceptChildNode)
                            self.reasonerDict[node].append(existentialConcept)
