import platform
import os
from pathlib import Path

import dependencies.py.utils.command4py as c4py
from dependencies.py.ramen import Lexer, TokenTypes, Parser

class RamenCLI(c4py.Program):
	
	@c4py.command(description="Compile your Ramen program into NekoVM's binaries")
	def compile(self, name: str, output: str = "a"):
		output += ".neko"
		ramen_neko_api = str(Path.cwd() / "deps" / "nekoramen" / "ramen.neko")
		
		programAST = None
		with open(name, "r") as file:
			l = Lexer(file.read())
			tokens = l.parse_tokens()
			programAST = Parser(tokens).parse_ast()

		source = programAST.as_neko()

		with open(ramen_neko_api, "r") as rnapisrc:
			source = rnapisrc.read() + "\n\n" + source

		with open(output, "w") as ofile:
			ofile.write(source + "\n\n Main()") # This will make our Ramen Program should always need the main function


	@c4py.command(description="Run your Ramen program in NekoVM's binaries")
	def run(self, nekosource: str):
		nekocc = str(Path.cwd() / "deps" / "neko_win64" / "nekoc")
		nekort = str(Path.cwd() / "deps" / "neko_win64" / "neko")

		nekosourcename = ".".join(nekosource.split(".")[:-1]) # This will take off the extension
		nekobin = nekosourcename + ".n"
		os.system(f"{nekocc} {nekosource}")
		os.system(f"{nekort} {nekobin}")
		os.system(f"del {nekobin}")

c4py.run(RamenCLI)