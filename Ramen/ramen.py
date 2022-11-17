import platform
from pathlib import Path

import utils.command4py as c4py
from ramen import RamenEnv

import settings

class RamenCLI(c4py.Program):
	env = RamenEnv(Path(settings.ROOT) / "dependencies")
	
	@c4py.command(description="Build your Project")
	def build(self, projectdir: str, output: str = "a"):
		self.env.build_project(projectdir)

	@c4py.command(description="Run your Ramen program in NekoVM's binaries")
	def run(self, nekosource: str):
		self.env.run(nekosource)

c4py.run(RamenCLI)