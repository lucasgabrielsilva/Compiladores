import sys
from lexica import Lexica

def main():
	if(len(sys.argv) < 2):
		print("ERRO - Por Favor Informe Um Arquivo .tpp")
	else:
		try:
			lexer = Lexica()
			lexer.readFile(sys.argv[1])
			lexer.printTokens()
		except:
			print("ERRO - Nao Foi Possivel Executar a Função, Por Favor Tente Novamente")

if __name__ == "__main__":
	main()