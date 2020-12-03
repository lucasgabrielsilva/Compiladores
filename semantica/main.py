import sys
from graphviz import Digraph
from lexica import Lexica
from sintatica import Sintatica
from semantica import Semantica
from tree import Tree

def main():
	if(len(sys.argv) < 2):
		print("ERRO - Por Favor Informe Um Arquivo .tpp")
	else:
			file = open(sys.argv[1], 'r', encoding='utf-8')
			sin = Sintatica(file.read(), Lexica().tokens)
			#dot = Digraph(comment='TREE')
			#Tree().printTree(sin.ast, dot)
			#dot.render('out/sintatica/normal.gv', view=True)
			Tree().poda(sin.ast)
			#dot = Digraph(comment='TREE')
			#Tree().printTreeCut(sin.ast, dot)
			#dot.render('out/semantica/poda.gv', view=True)
			sema = Semantica()
			sema.percorrerTree(sin.ast)
			sema.verificacoes()
			#sema.printTabSymbols()
	

if __name__ == "__main__":
	main()
