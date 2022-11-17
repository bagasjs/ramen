import glob
from pathlib import Path
import os

from .lexer import Lexer
from .token import TokenTypes
from .ast import Parser
from .bundler import Bundler

class RamenEnv:
	FILE_EXT = "ramen"
	NEKO_EXT = "bin"

	def __init__(self, ramen_home: Path|str):
		ramen_home = Path(ramen_home)
		self.nekovm = ramen_home / "neko_win64" / "neko"
		self.nekoc = ramen_home / "neko_win64" / "nekoc"

		dependencies = [
			ramen_home / "nekoramen" / "builtins.neko",
		]

		self.nbundler = Bundler() # The Neko Sources Bundler
		self.nbundler.from_files(dependencies)
		self.rbundler = Bundler() # Ramen Bundler

	def build_project(self, projectpath: Path|str):
		if not os.path.isdir(projectpath):
			raise FileNotFoundError(projectpath)
		projectpath = Path(projectpath) 
		psfs = self._search_ramen_from_path(Path.cwd() / projectpath) # Project Source Files
		self.rbundler.from_files(psfs)
		l = Lexer(self.rbundler.get_bundled())
		p = Parser(l.parse_tokens())
		program = p.parse_ast()
		self.nbundler.from_source(program.as_neko())
		self.nbundler.from_source("Main()")
		
		self.nbundler.save_to(projectpath.name+f".{self.NEKO_EXT}")

	def run(self, projectname: str):
		os.system(f"{self.nekoc} {projectname}.bin")
		os.system(f"{self.nekovm} {projectname}.n")
		os.system(f"del {projectname}.n")


	def _search_ramen_from_path(self, path: Path|str):
		# This method will search every ramen file in a project recursively
		path = Path(path)
		return glob.glob(str(path / f"**/*.{self.FILE_EXT}"), recursive=True)
