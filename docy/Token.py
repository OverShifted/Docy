from enum import Enum

class TokenType(Enum):
	
	BeginHeader = 1
	EndHeader = 2

	Text = 7

	BeginItalic = 8
	EndItalic = 9

	BeginBold = 10
	EndBold = 11

	CodeBlock = 12
	InlineCodeBlock = 13

	BeginUnorderedList = 14
	BeginUnorderedListItem = 15
	EndUnorderedListItem = 16
	EndUnorderedList = 17

	Image = 18
	Link = 19

class Token:

	def __init__(self, tokenType, tokenValue):
		self.TokenType = tokenType
		self.TokenValue = tokenValue
