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
		try:
			file = open(sys.argv[1], 'r', encoding='utf-8')
			sin = Sintatica(file.read(), Lexica().tokens)
			sema = Semantica(sin.ast)
			#sema.printTabSimbolos()
		except Exception as e:
			print(e)
			print("ERRO - Nao Foi Possivel Executar a Funcao, Por Favor Tente Novamente")

if __name__ == "__main__":
	main()
