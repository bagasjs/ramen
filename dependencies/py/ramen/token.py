from __future__ import annotations

class Token:
	def __init__(self, type: TokenTypes, literal: str):
		self.type = type
		self.literal = literal

	def __str__(self):
		return f"{TokenTypes.where_value(self.type)}\t\t:\t{self.literal}"

class Enum:
	def __init__(self, items: list[str]):
		self.__items = items
		for i, value in enumerate(items):
			setattr(self, value, i)

	def where_value(self, value: int):
		return self.__items[value]


TokenTypes = Enum([
	# Single character tokens
		"TOK_PLUS",
		"TOK_MINUS",
		"TOK_ASTERISK",
		"TOK_SLASH",
		"TOK_LPAREN",
		"TOK_RPAREN",
		"TOK_LBRACE", # {
		"TOK_RBRACE", # }
		"TOK_LBRACKET", # [
		"TOK_RBRACKET", # ]

		"TOK_DOT",
		"TOK_COMMA",
		"TOK_SEMICOLON",

	# Single or double character tokens
		"TOK_ASSIGN",
		"TOK_EQ",
		"TOK_BANG",
		"TOK_NEQ",
		"TOK_LT",
		"TOK_LTE",
		"TOK_GT",
		"TOK_GTE",

	# Keywords
		"TOK_OR",
		"TOK_AND",
		"TOK_VAR",
		"TOK_CONST",
		"TOK_IF",
		"TOK_ELSE",
		"TOK_REPEAT",
		"TOK_BREAK",
		"TOK_CONTINUE",
		"TOK_TRUE",
		"TOK_FALSE",
		"TOK_FUNCTION",
		"TOK_RETURN",
		"TOK_PACKAGE",
		"TOK_DOLLAR",

	# Literals
		"TOK_STRING",
		"TOK_INT",
		"TOK_FLOAT",
		"TOK_BOOL",

		"TOK_IDENTIFIER",
		"TOK_INVALID",
		"TOK_EOF",
])