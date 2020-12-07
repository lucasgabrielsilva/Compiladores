import sys
from graphviz import Digraph
from lexica import Lexica
from sintatica import Sintatica
from semantica import Semantica
from tree import Tree
from geracao import Geracao
#from gen2 import Geracao
from llvmlite import ir
from llvmlite import binding as llvm


def main():
	if(len(sys.argv) < 2):
		print("ERRO - Por Favor Informe Um Arquivo .tpp")
	else:
			file = open(sys.argv[1], 'r', encoding='utf-8')
			sin = Sintatica(file.read(), Lexica().tokens)
			dot = Digraph(comment='TREE')
			Tree().printTree(sin.ast, dot)
			#dot.render('out/sintatica/normal.gv', view=True)
			Tree().poda(sin.ast)
			dot = Digraph(comment='TREE')
			Tree().printTreeCut(sin.ast, dot)
			#dot.render('out/semantica/poda.gv', view=True)
			sema = Semantica()
			sema.percorrerTree(sin.ast)
			sema.verificacoes()
			#sema.printTabSymbols()
			llvm.initialize()
			llvm.initialize_all_targets()
			llvm.initialize_native_target()
			llvm.initialize_native_asmparser()
			modulo = ir.Module(sys.argv[1])
			modulo.triple = llvm.get_process_triple()
			target = llvm.Target.from_triple(modulo.triple)
			targetMachine = target.create_target_machine()
			modulo.data_layout = targetMachine.target_data
			Geracao().percorrer(sin.ast, modulo)
			arquivo = open('teste.ll', 'w')
			arquivo.write(str(modulo))
			arquivo.close()
			print(modulo)
	

if __name__ == "__main__":
	main()
