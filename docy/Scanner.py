from docy import Token

class Scanner:

	def __init__(self, source):
		self.Source = source

	def ScanTokens(self):
		self.Tokens = list()

		is_italic = False
		is_bold = False

		current_header = 0
		in_ulist = False

		pos = 0
		while pos < len(self.Source):

			char = self.Source[pos]

			if char == '\n':
				if current_header != 0:
					self.Tokens.append(Token.Token(Token.TokenType.EndHeader, current_header))
					current_header = 0
				elif in_ulist:
					self.Tokens.append(Token.Token(Token.TokenType.EndUnorderedListItem, None))
					if self.Source[pos + 1 : pos + 3] != "* ":
						in_ulist = False
						self.Tokens.append(Token.Token(Token.TokenType.EndUnorderedList, None))


			if (pos == 0 or self.Source[pos - 1] == '\n') and char == '#':
				pos += 1
				hash_count = 1
				char = self.Source[pos]
				while char == '#':
					pos += 1
					hash_count += 1
					char = self.Source[pos]

				if char == ' ':
					self.Tokens.append(Token.Token(Token.TokenType.BeginHeader, hash_count))
					current_header = hash_count

			elif (pos == 0 or self.Source[pos - 1] == '\n') and self.Source[pos : pos + 3] == '```':
				pos = self.CodeBlock(pos + 3)

			elif (pos == 0 or self.Source[pos - 1] == '\n') and self.Source[pos : pos + 2] == '* ':
				if not in_ulist:
					in_ulist = True
					self.Tokens.append(Token.Token(Token.TokenType.BeginUnorderedList, None))
				self.Tokens.append(Token.Token(Token.TokenType.BeginUnorderedListItem, None))
				pos += 1

			else:
				if self.Source[pos : pos + 3] == '***' or self.Source[pos : pos + 3] == '___': # bold and italic
					if not is_bold and not is_italic:
						self.Tokens.append(Token.Token(Token.TokenType.BeginBold, None))
						self.Tokens.append(Token.Token(Token.TokenType.BeginItalic, None))
					else:
						self.Tokens.append(Token.Token(Token.TokenType.EndItalic, None))
						self.Tokens.append(Token.Token(Token.TokenType.EndBold, None))
					is_bold = not is_bold
					pos += 2

				elif (self.Source[pos : pos + 2] == '**' or self.Source[pos : pos + 2] == '__') and self.Source[pos + 1] != ' ': # bold
					if is_bold:
						self.Tokens.append(Token.Token(Token.TokenType.EndBold, None))
					else:
						self.Tokens.append(Token.Token(Token.TokenType.BeginBold, None))
					is_bold = not is_bold
					pos += 1

				elif (self.Source[pos] == '*' or self.Source[pos] == '_') and self.Source[pos + 1] != ' ': # italic
					if is_italic:
						self.Tokens.append(Token.Token(Token.TokenType.EndItalic, None))
					else:
						self.Tokens.append(Token.Token(Token.TokenType.BeginItalic, None))
					is_italic = not is_italic

				elif self.Source[pos] == '`' or self.Source[pos : pos + 2] == '``' or self.Source[pos : pos + 3] == '```':
					pos = self.InlineCodeBlock(pos)

				elif self.Source[pos : pos + 2] == '![':
					pos = self.Image(pos)

				elif self.Source[pos] == '[':
					pos = self.Link(pos)

				else:
					self.Tokens.append(Token.Token(Token.TokenType.Text, self.Source[pos]))

			pos += 1

	def CodeBlock(self, pos):
		start = pos
		while pos + 3 < len(self.Source) and self.Source[pos : pos + 3] != '```':
			pos += 1

		self.Tokens.append(Token.Token(Token.TokenType.CodeBlock, self.Source[start : pos]))
		pos += 2
		return pos
	
	def UList(self, pos):
		self.Tokens.append(Token.Token(Token.TokenType.BeginUnorderedList, None))
		while pos < len(self.Source):
			if (pos == 0 or self.Source[pos - 1] == '\n') and self.Source[pos : pos + 2] == '* ':
				pos += 2
				item = ""
				while pos < len(self.Source) and self.Source[pos] != '\n':
					item += self.Source[pos]
					pos += 1
				self.Tokens.append(Token.Token(Token.TokenType.UnorderedListItem, item))
			else:
				break
			pos += 1
		self.Tokens.append(Token.Token(Token.TokenType.EndUnorderedList, None))

		return pos - 1

	def InlineCodeBlock(self, pos):
		literal = '`'
		if self.Source[pos : pos + 2] == '``':
			literal = '``'
		elif self.Source[pos : pos + 3] == '```':
			literal = '```'

		pos += len(literal)
		start = pos
		while pos + len(literal) < len(self.Source) and self.Source[pos : pos + len(literal)] != literal:
			pos += 1

		self.Tokens.append(Token.Token(Token.TokenType.InlineCodeBlock, self.Source[start : pos]))
		return pos

	def Image(self, pos):
		name_start = pos + 2
		while self.Source[pos : pos + 2] != '](':
			pos += 1
		name_end = pos
		link_start = pos + 2
		while pos < len(self.Source) and self.Source[pos] != ')':
			pos += 1
		self.Tokens.append(Token.Token(Token.TokenType.Image, self.Source[link_start : pos]))
		return pos

	def Link(self, pos):
		name_start = pos + 1
		while self.Source[pos : pos + 2] != '](':
			pos += 1
		name_end = pos
		link_start = pos + 2
		while pos < len(self.Source) and self.Source[pos] != ')':
			pos += 1
		self.Tokens.append(Token.Token(Token.TokenType.Link, [self.Source[name_start : name_end], self.Source[link_start : pos]]))
		return pos
