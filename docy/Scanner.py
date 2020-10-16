import Token

class Scanner:

	def __init__(self, source):
		self.Source = source

	def ScanTokens(self):
		self.Tokens = list()

		is_italic = False
		is_bold = False

		pos = 0
		while pos < len(self.Source):

			char = self.Source[pos]

			if (pos == 0 or self.Source[pos - 1] == '\n') and char == '#':
				pos += 1
				hash_count = 1
				char = self.Source[pos]
				while char == '#':
					pos += 1
					hash_count += 1
					char = self.Source[pos]

				if char == ' ':
					start = pos
					while pos < len(self.Source) and char != '\n':
						pos += 1
						char = self.Source[pos]
					self.Header(hash_count, start + 1, pos)
					pos -= 1
					char = self.Source[pos]

			elif pos == 0 or self.Source[pos - 1] == '\n' and self.Source[pos : pos + 3] == '```':
				pos = self.CodeBlock(pos + 3)

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

				elif self.Source[pos : pos + 2] == '**' or self.Source[pos : pos + 2] == '__': # bold
					if is_bold:
						self.Tokens.append(Token.Token(Token.TokenType.EndBold, None))
					else:
						self.Tokens.append(Token.Token(Token.TokenType.BeginBold, None))
					is_bold = not is_bold
					pos += 1

				elif self.Source[pos] == '*' or self.Source[pos] == '_': # italic
					if is_italic:
						self.Tokens.append(Token.Token(Token.TokenType.EndItalic, None))
					else:
						self.Tokens.append(Token.Token(Token.TokenType.BeginItalic, None))
					is_italic = not is_italic

				else:
					self.Tokens.append(Token.Token(Token.TokenType.Text, self.Source[pos]))

			pos += 1

	def Header(self, level, start, end):
		attr = getattr(Token.TokenType, "H" + str(level))
		self.Tokens.append(Token.Token(attr, self.Source[start : end]))

	def CodeBlock(self, pos):
		start = pos
		while pos + 3 < len(self.Source) and self.Source[pos : pos + 3] != '```':
			pos += 1

		self.Tokens.append(Token.Token(Token.TokenType.CodeBlock, self.Source[start : pos]))
		return pos
