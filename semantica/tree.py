class Tree:
    def __init__(self, type_node='', child=[], value='', linha=''):
        self.type = type_node
        self.child = child
        self.value = value
        self.linha = linha

    def __str__(self):
        return self.type
    
    def printTree(self, node, dot, i="0", pai=None):
        if node != None:
            filho = str(node) + str(i)
            dot.node(filho, str(node))
            if pai: dot.edge(pai, filho)
            j = "0"
            if not isinstance(node, Tree): return
            for son in node.child:
                j+="1"
                self.printTree(son, dot, i+j, filho)
    
    def poda(self, no):
        self.cut(no)
        self.cut2(no)
    
    def cut(self, no):
        if no != None:
            if not isinstance(no, Tree):
                return
            for soon in no.child:
                self.cut(soon)
                if soon.type == "expressao_logica":
                    lfs = []
                    self.get(soon, lfs)
                    for l in lfs:
                        no.child.append(l)
                    no.child.remove(soon)
                if soon.type == "vazio" and no.type == "corpo":
                    no.child.remove(soon)
                if soon.type == "declaracao":
                    for i in soon.child:
                        no.child.append(i)
                    no.child.remove(soon)
                if soon.type == "expressao" and (no.type == "indice" or no.type == "escreva"):
                    for i in soon.child:
                        no.child.append(i)
                    no.child.remove(soon)
                for grand in soon.child:
                    if grand.type == "atribuicao" and soon.type == "expressao" and no.type == "atribuicao":
                        for g in grand.child:
                            no.child.append(g)
                        no.child.remove(soon)
                    if no.type == "corpo" and soon.type == "acao" and grand.type == "expressao":
                        no.child.append(grand.child[0])
                        no.child.remove(soon)

    def cut2(self, no):
        if no != None:
            if not isinstance(no, Tree):
                return
            for soon in no.child:
                if soon.type == no.type:
                    for i in soon.child:
                        no.child.insert(0, i)
                    no.child.remove(soon)
                    self.cut2(no)
                if soon.type == "acao" and no.type == "corpo":
                    for i in soon.child:
                        no.child[no.child.index(soon)] = i
                self.cut2(soon)


    def get(self, no, values=[]):
        if no:
            for soon in no.child:
                if soon.type == "chamada_funcao":
                    values.append(soon)
                    return
                if soon.type == "indice":
                    return
                if soon.value:
                    values.append(soon)
                self.get(soon, values)

    def printTreeCut(self, node, dot, i="0", pai=None):
        if node != None:
            soon = str(node) + str(i)
            dot.node(soon, str(node))
            if pai:
                dot.edge(pai, soon)
            j = "0"
            if not isinstance(node, Tree):
                return
            for son in node.child:
                j += "1"
                self.printTreeCut(son, dot, i+j, soon)