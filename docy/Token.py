from enum import Enum

class TokenType(Enum):
	
	# Headers
	H1 = 1
	H2 = 2
	H3 = 3
	H4 = 4
	H5 = 5
	H6 = 6

	Text = 7

	BeginItalic = 8
	EndItalic = 9

	BeginBold = 10
	EndBold = 11

	CodeBlock = 12

class Token:

	def __init__(self, tokenType, tokenValue):
		self.TokenType = tokenType
		self.TokenValue = tokenValue
