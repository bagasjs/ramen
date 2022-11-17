from .token import Token, TokenTypes

class Lexer:

	keywords_map = {
		"or" : TokenTypes.TOK_OR,
		"and" : TokenTypes.TOK_AND,
		"var" :	TokenTypes.TOK_VAR,
		"const" : TokenTypes.TOK_CONST,
		"if" : TokenTypes.TOK_IF,
		"else" : TokenTypes.TOK_ELSE,
		"repeat" : TokenTypes.TOK_REPEAT,
		"break" : TokenTypes.TOK_BREAK,
		"continue" : TokenTypes.TOK_CONTINUE,
		"true" : TokenTypes.TOK_TRUE,
		"false" : TokenTypes.TOK_FALSE,
		"fun" : TokenTypes.TOK_FUNCTION,
		"pack" : TokenTypes.TOK_PACKAGE,
		"return" : TokenTypes.TOK_RETURN,
		"debugbreak" : TokenTypes.TOK_EOF
	}

	def __init__(self, source_code: str):
		self.current = 0
		self.next = 0
		self.source_code = source_code + "\ndebugbreak;"
		self._cchar = None
		self._nchar = None
		self.next_char()

	def skip_whitespace(self):
		while self.cchar in [ " ",  "\t", "\n", "\v", "\f" ]:
			self.next_char()

	def next_char(self):
		self.current = self.next
		self.next += 1

	@property
	def cchar(self):
		if self._cchar != self.source_code[self.current]:
			self._cchar = self.source_code[self.current]
		return self._cchar

	@property
	def nchar(self):
		if self._nchar != self.source_code[self.next]:
			self._nchar = self.source_code[self.next]
		return self._nchar

	@classmethod
	def is_alpha(self, char: str):
		return char.isalpha()

	@classmethod
	def is_digit(self, char: str):
		return char.isdigit()

	@classmethod
	def is_alphanumeric(self, char: str):
		return char.isalnum()

	def read_string(self):
		writer = ""
		while self.cchar != "\"":
			writer += self.cchar
			self.next_char()
		return writer

	def skip_comment(self):
		if self.cchar != "#":
			return
		while self.cchar != "\n":
			self.next_char()

	def read_float(self):
		writer = ""
		has_dot = False
		while self.is_digit(self.cchar) or self.cchar == ".":
			if self.cchar == "." and has_dot:
				return None
			writer += self.cchar
			self.next_char()
		return writer

	def read_keyword(self):
		writer = ""
		while self.is_alphanumeric(self.cchar):
			writer += self.cchar
			if not self.is_alphanumeric(self.nchar):
				break
			self.next_char()
		return writer

	i = 1

	def next_token(self):
		if self.current >= len(self.source_code):
			return Token(TokenTypes.TOK_EOF, "")

		self.skip_comment()
		self.skip_whitespace()

		token = None
		# Single character tokens
		token = Token(TokenTypes.TOK_COMMA, ",") if self.cchar == "," else token
		token = Token(TokenTypes.TOK_DOLLAR, "$") if self.cchar == "$" else token
		token = Token(TokenTypes.TOK_DOT, ".") if self.cchar == "." else token
		token = Token(TokenTypes.TOK_PLUS, "+") if self.cchar == "+" else token
		token = Token(TokenTypes.TOK_MINUS, "-") if self.cchar == "-" else token
		token = Token(TokenTypes.TOK_SLASH, "/") if self.cchar == "/" else token
		token = Token(TokenTypes.TOK_ASTERISK, "*") if self.cchar == "*" else token
		token = Token(TokenTypes.TOK_LPAREN, "(") if self.cchar == "(" else token
		token = Token(TokenTypes.TOK_RPAREN, ")") if self.cchar == ")" else token
		token = Token(TokenTypes.TOK_LBRACE, "{") if self.cchar == "{" else token
		token = Token(TokenTypes.TOK_RBRACE, "}") if self.cchar == "}" else token
		token = Token(TokenTypes.TOK_LBRACKET, "[") if self.cchar == "[" else token
		token = Token(TokenTypes.TOK_RBRACKET, "]") if self.cchar == "]" else token
		token = Token(TokenTypes.TOK_SEMICOLON, ";") if self.cchar == ";" else token

		# Single or Double character tokens
		if self.cchar == "=":
			if self.nchar == "=":
				token = Token(TokenTypes.TOK_EQ, self.cchar + self.nchar)
				self.next_char()
				self.next_char()
			else:
				token = Token(TokenTypes.TOK_ASSIGN, self.cchar)
				self.next_char()

		if self.cchar == "!" :
			if self.nchar == "=":
				token = Token(TokenTypes.TOK_NEQ, self.cchar + self.nchar)
				self.next_char()
				self.next_char()
			else:
				token = Token(TokenTypes.TOK_BANG, self.cchar)
				self.next_char()

		if self.cchar == ">": 
			if self.nchar == "=":
				token = Token(TokenTypes.TOK_GTE, self.cchar + self.nchar)
				self.next_char()
				self.next_char()
			else:
				token = Token(TokenTypes.TOK_GT, self.cchar)
				self.next_char()

		if self.cchar == "<": 
			if self.nchar == "=":
				token = Token(TokenTypes.TOK_LTE, self.cchar + self.nchar)
				self.next_char()
				self.next_char()
			else:
				token = Token(TokenTypes.TOK_LT, self.cchar)
				self.next_char()

		if self.cchar == "\"":
			self.next_char() # skip the "
			res = self.read_string()
			token = Token(TokenTypes.TOK_STRING, res) if res != None else Token(TokenTypes.TOK_INVALID, "")
			self.next_char()
			return token

		if self.is_alpha(self.cchar):
			res = self.read_keyword()
			type = TokenTypes.TOK_IDENTIFIER if res not in self.keywords_map.keys() else self.keywords_map[res]
			token = Token(type, res) if res != None else Token(TokenTypes.TOK_INVALID, "")
			self.next_char()
			return token

		if self.is_digit(self.cchar):
			res = self.read_float()
			type = TokenTypes.TOK_FLOAT if "." in res else TokenTypes.TOK_INT
			token = Token(type, res) if res != None else Token(TokenTypes.TOK_INVALID, "")
			return token

		token = Token(TokenTypes.TOK_INVALID, "") if token == None else token
		self.next_char()
		return token

	def parse_tokens(self):
		tokens = []
		token = self.next_token()
		while token.type != TokenTypes.TOK_EOF:
			if token.type == TokenTypes.TOK_INVALID:
				raise Exception("Invalid Token Found")
			tokens.append(token)
			token = self.next_token()
		return tokens