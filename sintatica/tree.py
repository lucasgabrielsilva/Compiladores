class Tree:
    def __init__(self, type_node='', child=[], value='', line=''):
        self.type = type_node
        self.child = child
        self.value = value
        self.lineno = line
        self.j = 1

    def __str__(self):
        return self.type

    def printTree(self, node, sonStr, father, w, i):
        if(node != None):
            i += 1
            father = str(node) + " " + str(i-1) + " " + str(self.j-1)
            for son in node.child:
                sonStr = str(son) + " " + str(i) + " " + str(self.j)
                w.edge(father, sonStr)
                self.j += 1
                self.printTree(son, sonStr, father, w, i)
