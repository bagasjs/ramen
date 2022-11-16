import inspect
from abc import ABCMeta
from argparse import ArgumentParser

# --- Utilities
def eliminate_none_items(d: dict):
	res = {}
	for key, value in d.items():
		if value == None:
			continue
		res[key] = value
	return res

# ---\ 



class Command:
	# description describe the command
	# help describe the arguments that's received
	def __init__(self, callback, description = None, help = None):
		self.name = self.refine_name(callback.__name__)
		self.callback = callback
		self.description = description
		self.help = {} if help == None else help

	def refine_name(self, name: str):
		name = name.replace("_", "-")
		name = name.lower()
		return name

	@classmethod
	def create_command(cls, *a, **kw):
		def _command(callback):
			return cls(callback, *a, **kw)
		return _command

	def __call__(self, *args, **kwargs):
		return self.callback(*args, **kwargs)

class DefaultConfig:
	description = None


class ProgramMeta(ABCMeta):
	def __new__(cls, name: str, bases: tuple, attrs: dict, **kw):
		super_new = super().__new__
		commands = []
		for _, attr in attrs.items():
			if isinstance(attr, Command):
				commands.append(attr)

		config_class = attrs.pop("Config", DefaultConfig)
		config = config_class()
	
		config.commands = commands
		if not hasattr(config, "name"):
			setattr(config, "name", name)
			attrs["_config"] = config

		return super_new(cls, name, bases, attrs, **kw)


class Program(metaclass=ProgramMeta):
	def __getitem__(self, __k):
		return getattr(self._config, __k)


def get_parser(program):
	kwargs = {
		"description" : program["description"]
	}
	kwargs = eliminate_none_items(kwargs)
	parser = ArgumentParser(**kwargs)
	subparsers = parser.add_subparsers(title="Commands", description="List of available commands", dest="command_name")

	for command in program["commands"]:
		# Creating the command parser
		kwargs = {
			"help" : command.description,
		}
		kwargs = eliminate_none_items(kwargs)
		command_parser = subparsers.add_parser(command.name, **kwargs)
		
		# Getting the configuration and adding it to the command parser
		used_shorthands = []
		parameters = inspect.signature(command.callback).parameters

		for i, parameter in enumerate(parameters.values()):
			# Just skip the first parameter because it's usually self
			if i == 0:
				continue

			names = [parameter.name]
			configs = {}


			# Checking if the arguments is optional or required
			if parameter.default != inspect._empty:
				configs["metavar"] = ""
				names[0] = "--" + parameter.name
				shorthand = names[0][0]
				if shorthand not in used_shorthands:
					names.append("-" + parameter.name[0])
				configs["default"] = parameter.default

				# Checking if the parameter has help
				if command.help and parameter.name in command.help:
					configs["help"] = command.help[parameter.name]

			# ToDo: Add the type conversion feature by checking the annotations and add it to the configs
			command_parser.add_argument(*names, **configs)
	return parser

def run(prog_class: ProgramMeta):
	prog = prog_class()
	parser = get_parser(prog)
	args = parser.parse_args()
	if not args.command_name:
		return
	command = getattr(prog, args.command_name)
	
	kw = {}
	for i, parameter in enumerate(inspect.signature(command.callback).parameters.values()):
		if hasattr(args, parameter.name):
			kw[parameter.name] = getattr(args, parameter.name)
	command(prog, **kw)


command = Command.create_command
__all__ = [
	"command",
	"Program",
	"run"
]