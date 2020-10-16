import sys
import argparse

import Scanner, Token

def main():
	html_file = open("out.html", 'w');
	md_file = open("test.md", 'r');
	scanner = Scanner.Scanner(md_file.read())
	scanner.ScanTokens()

	html_file.write('<html>\n\t<head>\n\t\t<link rel="stylesheet" href="docy/styles/main_style.css">\n\t</head>\n\t<body>\n')

	for token in scanner.Tokens:
		if 7 > token.TokenType.value > 0:
			html_file.write("\t\t<h{level}>{value}</h{level}>".format(level = token.TokenType.value, value = token.TokenValue))
		elif token.TokenType == Token.TokenType.CodeBlock:
			html_file.write("\t\t<p>{value}</p>\n".format(value = token.TokenValue.replace("\n", "<br/>\n")))

		elif token.TokenType == Token.TokenType.Text:
			html_file.write(token.TokenValue)

		elif token.TokenType == Token.TokenType.BeginItalic:
			html_file.write("<i>")
		elif token.TokenType == Token.TokenType.EndItalic:
			html_file.write("</i>")

		elif token.TokenType == Token.TokenType.BeginBold:
			html_file.write("<b>")
		elif token.TokenType == Token.TokenType.EndBold:
			html_file.write("</b>")

	html_file.write("\n\t</body>\n</html>")

	md_file.close()
	html_file.close()

if __name__ == '__main__':
	main()
