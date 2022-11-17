from __future__ import annotations
from abc import ABC, abstractmethod

from .token import TokenTypes, Token

class AST(ABC):
	@abstractmethod
	def string(self):
		pass

	@abstractmethod
	def as_neko(self):
		pass

	def __str__(self):
		return self.string()

	def __repr__(self):
		return self.string()

class Program(AST):
	def __init__(self, body: list[AST]):
		self.body = body

	def string(self):
		writer = ""
		for b in self.body:
			writer += str(b) + "\n"
		return writer

	def as_neko(self):
		writer = ""
		for b in self.body:
			writer += b.as_neko()
		return writer

# Actually for literal value
class Value(AST):
	def __init__(self, token: Token|ArrayList):
		self.value = token.literal
		self.type = token.type if token.type not in [TokenTypes.TOK_TRUE, TokenTypes.TOK_FALSE] else TokenTypes.TOK_BOOL

	def string(self):
		return self.value if self.type != TokenTypes.TOK_STRING else f"\"{self.value}\""

	def as_neko(self):
		return self.string()

class Identifier(AST):
	def __init__(self, token: Token):
		self.name = token.literal

	def string(self):
		return self.name

	def as_neko(self):
		return self.string()

class ArrayList(AST):
	def __init__(self, items: list[Value|Identifier]):
		self.items = items

	def string(self):
		raise Exception("what")
		return "["+", ".join([str(item) for item in self.items])+"]"

	def as_neko(self):
		return "$array("+", ".join([str(item) for item in self.items])+")"

class HashMap(AST):
	def __init__(self, pairs: list[ValueDefinition]):
		self.pairs = pairs

	def string(self):
		return "["+", ".join([str(p) for p in self.pairs])+"]"

	def as_neko(self):
		pairs = []
		for pair in self.pairs:
			pairs.append(pair.left.as_neko() + " => " + pair.right.as_neko())
		return "{"+",".join([str(p) for p in pairs])+"}"

"""
Indexing AST is used for getting a value in an arraylist or hashmap
e.g:
users[0][name] 
blogs[1]["title"]
"""
class Indexing(AST):
	def __init__(self, identifier: Identifier, args: list[Value|Identifier]):
		self.identifier = identifier
		self.args = args

	def string(self):
		return f"{self.identifier}{''.join(['['+str(a)+']' for a in self.args])}"

	def as_neko(self):
		return self.string()

class HashMapIndexing(Indexing):
	pass

# var x
class VariableDeclaration(AST):
	def __init__(self, identifier: Identifier):
		self.identifier = identifier

	def string(self):
		return f"var {self.identifier}"

	def as_neko(self):
		return self.string()


# x = 1
class ValueDefinition(AST):
	def __init__(self, left: Identifier, right: Value|Identifier|ArrayList|HashMap|FunctionCall):
		self.left = left
		self.right = right

	def string(self):
		return f"{self.left} = {self.right}"

	def as_neko(self):
		return f"{self.left.as_neko()} = {self.right.as_neko()};"

# var x = 1
class VariableInitialization(AST):
	def __init__(self, valuedef: ValueDefinition):
		self.valuedef = valuedef
		self.vardec = VariableDeclaration(self.valuedef.left)

	def string(self):
		return "var " + str(self.valuedef)

	def as_neko(self):
		return "var "  + self.valuedef.as_neko()

class BlockStatement(AST):
	def __init__(self, body: list[AST]):
		self.body = body

	def string(self):
		writer = "{\n"
		for b in self.body:
			writer += str(b) + "\n"
		return writer + "}"

	def as_neko(self):
		writer = "{\n"
		for b in self.body:
			writer += b.as_neko() + "\n"
		return writer + "}"

"""
This will be the arguments that's need to be handled by a function e.g ("localhost", 8080)
The function arguments syntax will be different with the parameters syntax where you need to set the var keyword in parameter e.g
fun getRandomCallback(var host var port)
The reason of creating this in a separate AST is because we want to call a function after another function call for example
getRandomCallback("localhost", 8080)();
"""
class FunctionArgs(AST):
	def __init__(self, arguments: list[Value|Identifier]):
		self.arguments = arguments

	def string(self):
		return f"({','.join([str(a) for a in self.arguments])})".replace("\n", "")

	def as_neko(self):
		return self.string()

# x()
class FunctionCall(AST):
	def __init__(self, identifier: Identifier, args: list[FunctionArgs]):
		self.identifier = identifier
		self.arguments = args

	def string(self):
		return f"{self.identifier}{''.join([str(a) for a in self.arguments])}"

	def as_neko(self):
		return self.string()

class FunctionDefinition(AST):
	def __init__(self, identifier: Token, params: list[Identifier], body: BlockStatement):
		self.identifier = identifier
		self.params = params
		self.body = body

	def string(self):
		return f"fun {self.identifier}({','.join(['var ' + str(a) for a in self.params])}) {str(self.body)}"

	def as_neko(self):
		return f"var {self.identifier} = function({','.join([ a.as_neko() for a in self.params])}) {self.body.as_neko()}\n"

class LambdaFunction(AST):
	def __init__(self, params: list[identifier], body: BlockStatement):
		self.params = params
		self.body = body

	def string(self):
		raise Exception("What")
		return f"fun({','.join(['var ' + str(a) for a in self.params])}) {str(self.body)}"

	def as_neko(self):
		return f"function({','.join([a.as_neko() for a in self.params])}) {self.body.as_neko()}"


class ReturnStatemnt(AST):
	def __init__(self, value: Value|Identifier|Operation):
		self.value = value

	def string(self):
		return "return " + str(self.value)

	def as_neko(self):
		return self.value.as_neko() + ";"

class Operation(AST):
	def __init__(self, left: Identifier|Value, op: Token, right: Identifier|Value|Operation):
		self.left = left
		self.right = right
		self.op = op.literal

	def string(self):
		return f"{self.left} {self.op} {str(self.right)}"

	def as_neko(self):
		return self.string()

class Empty(AST):
	def string(self):
		return ""

	def as_neko(self):
		return self.string()

class Package(AST):
	def __init__(self, identifier: Identifier, body: BlockStatement):
		self.identifier = identifier
		self.body = body

	def string(self):
		return f"pack {self.identifier} {self.body}"

	def as_neko(self):
		return self.body.as_neko()

class RepeatStatement(AST):
	def __init__(self, body: BlockStatement):
		self.body = body

	def string(self):
		return f"repeat {self.body}"

	def as_neko(self):
		return f"while (true) {self.body}"

class BreakStatement(AST):
	def string(self):
		return "break"

	def as_neko(self):
		return self.string() + ";"

class ContinueStatement(AST):
	def string(self):
		return "continue"

	def as_neko(self):
		return self.string() + ";"

class IfStatement(AST):
	def __init__(self, condition: Operation, todo: BlockStatement, alternate: BlockStatement):
		self.condition = condition
		self.todo = todo
		self.alternate = alternate

	def string(self):
		return f"if ({self.condition}) {self.todo.as_neko()} else {self.alternate.as_neko()}"

	def as_neko(self):
		return self.string()

INDEXING_TOKENS = [ TokenTypes.TOK_INT, TokenTypes.TOK_STRING, TokenTypes.TOK_IDENTIFIER ]
LITERALS = [ TokenTypes.TOK_INT, TokenTypes.TOK_FLOAT, TokenTypes.TOK_TRUE, TokenTypes.TOK_FALSE, TokenTypes.TOK_STRING ]
OPERATORS = [ TokenTypes.TOK_PLUS, TokenTypes.TOK_MINUS, TokenTypes.TOK_ASTERISK, TokenTypes.TOK_SLASH, TokenTypes.TOK_EQ, TokenTypes.TOK_NEQ, TokenTypes.TOK_GT, TokenTypes.TOK_GTE, TokenTypes.TOK_LT, TokenTypes.TOK_LTE ]

class Parser:
	def __init__(self, tokens: list[Token]):
		self.current = 0
		self.tokens = tokens
		self.in_func_state = 0 # This will check if we are in a function or not
		self.in_loop_state = 0
		self.in_if_state = 0

		self.variables = []

		self.call_a_func = 0 # This will check if we are calling a function or not

	def parse_ast(self):
		programAST = Program([])
		while self.current < len(self.tokens):
			res = self.walk()
			programAST.body.append(res)
		return programAST

	def error(self, a):
		raise Exception(a)

	def next_token(self):
		self.current += 1

	@property
	def ctoken(self):
		if self.current >= len(self.tokens):
			return None
		return self.tokens[self.current]

	@property
	def ntoken(self):
		if self.current + 1 >= len(self.tokens):
			return None
		return self.tokens[self.current + 1]

	def xntoken(self, amount: int):
		if self.current + amount >= len(self.tokens):
			return None
		return self.tokens[self.current + amount]

	@property
	def btoken(self):
		if self.current - 1 < 0:
			return None
		return self.tokens[self.current - 1]
	
	# Walk return none by default that means it's error
	# If it's not returning None then the current token should change to be the next token
	def walk(self):
		if self.ctoken.type == TokenTypes.TOK_SEMICOLON:
			self.next_token()
			return Empty()

		if self.ctoken.type in LITERALS:
			res = Value(self.ctoken)
			self.next_token()
			if self.ctoken.type in OPERATORS:
				op = self.ctoken
				self.next_token()
				res = Operation(res, op, self.walk())
			return res

		if self.ctoken.type == TokenTypes.TOK_LBRACKET:
			self.next_token() # skip the [
			res = HashMap([]) if self.ntoken.type == TokenTypes.TOK_ASSIGN else ArrayList([])		
			while self.ctoken.type != TokenTypes.TOK_RBRACKET:
				if self.ntoken.type == TokenTypes.TOK_ASSIGN:
					if isinstance(res, ArrayList):
						self.error("You need key and value pair in a hashmap")
					else:
						res.pairs.append(self.walk())
				else:
					if isinstance(res, HashMap):
						self.error("You can't declare key and value pair in array")
					else:
						r = self.walk()
						res.items.append(r)
				if self.ctoken.type == TokenTypes.TOK_RBRACKET:
					self.next_token()
					break
				if self.ctoken.type != TokenTypes.TOK_COMMA:
					self.error("Every item in a hashmap or array should be divided by comma")
					
				self.next_token() # Skip the ,
			return res

		if self.ctoken.type == TokenTypes.TOK_LPAREN:
			if self.call_a_func == 0:
				self.error("Please identify which function you are calling")
			self.next_token() # Just skip the "("
			res = FunctionArgs([])
			while self.ctoken.type != TokenTypes.TOK_RPAREN:
				argument = self.walk()
				res.arguments.append(argument)
				if self.ctoken.type == TokenTypes.TOK_COMMA:
					self.next_token()
			self.next_token() # Just skip the ")"
			return res

		# Identifier
		if self.ctoken.type == TokenTypes.TOK_IDENTIFIER:
			res = Identifier(self.ctoken)
			self.next_token()

			# This part will handle operations
			if self.ctoken.type in OPERATORS:
				op = self.ctoken
				self.next_token() # Skip the operator
				res = Operation(res, op, self.walk())
			# This part will handle assignment
			elif self.ctoken.type == TokenTypes.TOK_ASSIGN:
				self.next_token()
				r = self.walk()
				if not isinstance(r, (Value, Identifier, ArrayList, HashMap, FunctionCall, Operation)):
					self.error("Invalid syntax")
				res = ValueDefinition(res, r)
			# This part will handle function calls
			elif self.ctoken.type == TokenTypes.TOK_LPAREN:
				self.call_a_func += 1
				func_args = []
				while self.ctoken.type == TokenTypes.TOK_LPAREN:
					func_args.append(self.walk())
				res = FunctionCall(res, func_args)
				self.call_a_func -= 1
			# This will check whether we are currently indexing an array/hashmap or defining an array
			elif self.ctoken.type == TokenTypes.TOK_LBRACKET and self.ntoken.type in INDEXING_TOKENS and self.xntoken(2).type == TokenTypes.TOK_RBRACKET:
				indexing_args = []
				while self.ctoken.type == TokenTypes.TOK_LBRACKET and self.ntoken.type in INDEXING_TOKENS and self.xntoken(2).type == TokenTypes.TOK_RBRACKET:
					self.next_token() # This will skip the [
					indexing_args.append(self.walk()) # This will parse the next token whether it's a value or identifier
					self.next_token() # This will skip the ]
				res = Indexing(res, indexing_args)
			else:
				pass

			return res

		if self.ctoken.type == TokenTypes.TOK_RETURN:
			if self.in_func_state == 0:
				self.error("Error")
			self.next_token()
			return ReturnStatemnt(self.walk())

		if self.ctoken.type == TokenTypes.TOK_LBRACE:
			res = BlockStatement([])
			self.next_token() # skip the "{"
			while(self.ctoken.type != TokenTypes.TOK_RBRACE):
				res.body.append(self.walk())
			self.next_token()
			return res

		# For Normal Function
		if self.ctoken.type == TokenTypes.TOK_FUNCTION and self.ntoken.type == TokenTypes.TOK_IDENTIFIER:
			self.next_token() # skip the keyword
			res = FunctionDefinition(Identifier(self.ctoken), [], None) # ctoken is the function name
			self.next_token()
			if self.ctoken.type == TokenTypes.TOK_LPAREN:
				self.next_token()
				while self.ctoken.type != TokenTypes.TOK_RPAREN:
					if self.ctoken.type == TokenTypes.TOK_VAR and self.ntoken.type == TokenTypes.TOK_IDENTIFIER:
						self.next_token() # Just skip the var keyword
						res.params.append(self.walk())
						if self.ctoken.type == TokenTypes.TOK_COMMA:
							self.next_token()
					else:
						self.error("Something went wrong")						
				self.next_token()
			self.in_func_state += 1
			if self.ctoken.type != TokenTypes.TOK_LBRACE:
				self.error("Function declaration without the body")
			res.body = self.walk()
			self.in_func_state -= 1
			return res

		# For Lambda function
		if self.ctoken.type == TokenTypes.TOK_FUNCTION:
			self.next_token() # skip the keyword
			params = []
			if self.ctoken.type == TokenTypes.TOK_LPAREN:
				self.next_token()
				while self.ctoken.type != TokenTypes.TOK_RPAREN:
					if self.ctoken.type == TokenTypes.TOK_VAR and self.ntoken.type == TokenTypes.TOK_IDENTIFIER:
						self.next_token() # Just skip the var keyword
						params.append(self.walk())
						if self.ctoken.type == TokenTypes.TOK_COMMA:
							self.next_token()
					else:
						self.error("Something went wrong")
				self.next_token()
			self.in_func_state += 1
			if self.ctoken.type != TokenTypes.TOK_LBRACE:
				self.error("Function declaration without the body")
			res = LambdaFunction(params, self.walk())
			self.in_func_state -= 1
			return res

		if self.ctoken.type == TokenTypes.TOK_PACKAGE:
			self.next_token() # Just skip the package keyword
			if self.ctoken.type != TokenTypes.TOK_IDENTIFIER:
				self.error("Failed to create package")
				
			res = Package(Identifier(self.ctoken), None)
			self.next_token()
			if self.ctoken.type != TokenTypes.TOK_LBRACE:
				self.error("Package that has no body is meaningless")
				
			res.body = self.walk()
			return res

		if self.ctoken.type == TokenTypes.TOK_REPEAT:
			self.next_token() # Just skip the repeat keyword
			if self.ctoken.type != TokenTypes.TOK_LBRACE:
				self.error("Repeat statement error")
				
			self.in_loop_state += 1
			body = self.walk()
			self.in_loop_state -= 1
			return RepeatStatement(body)

		if self.ctoken.type == TokenTypes.TOK_IF:
			self.next_token() # Just skip the if keyword
			if self.ctoken.type != TokenTypes.TOK_LPAREN:
				self.error("if statement error")
			self.next_token()
			condition = self.walk()
			self.next_token()
			self.in_if_state += 1
			if self.ctoken.type != TokenTypes.TOK_LBRACE:
				self.error("if statement error")
			todo = self.walk()
			branch = None
			if self.ctoken.type == TokenTypes.TOK_ELSE:
				self.next_token() # Just skip the else keyword
				if self.ctoken.type != TokenTypes.TOK_LBRACE:
					self.error("if statement error")
				branch = self.walk()
			self.in_if_state -= 1
			if not isinstance(condition, Operation):
				self.error("If statement error")
			branch = branch if branch != None else BlockStatement([])
			return IfStatement(condition, todo, branch)

		if self.ctoken.type == TokenTypes.TOK_BREAK:
			if self.in_func_state == 0:
				self.error("Error")
			self.next_token()
			return BreakStatement()

		if self.ctoken.type == TokenTypes.TOK_CONTINUE:
			if self.in_func_state == 0:
				self.error("Error")
			self.next_token()
			return ContinueStatement()

		if self.ctoken.type == TokenTypes.TOK_VAR:
			if self.ntoken.type != TokenTypes.TOK_IDENTIFIER:
				self.error("Invalid token after variable definition expecting an identifier")
			self.next_token() # pass the var keyword
			res = self.walk() # Get the identifier
			if isinstance(res, ValueDefinition):
				res = VariableInitialization(res)
				self.variables.append(res.vardec)
			else:
				res = VariableDeclaration(res)
				self.variables.append(res)
			return res

		return None