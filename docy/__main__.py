import sys
import argparse

from docy import Scanner, Token

def main():
	html_file = open("out.html", 'w');
	md_file = open("test.md", 'r');
	scanner = Scanner.Scanner(md_file.read())
	scanner.ScanTokens()

	html_file.write('<html>\n\t<head>\n\t\t<link rel="stylesheet" href="docy/styles/main_style.css">\n\t</head>\n\t<body>\n')

	for i, token in enumerate(scanner.Tokens):
		if token.TokenType == Token.TokenType.BeginHeader:
			html_file.write("\t\t<h{}>".format(token.TokenValue))
		elif token.TokenType == Token.TokenType.EndHeader:
			html_file.write("</h{}>".format(token.TokenValue))

		elif token.TokenType == Token.TokenType.CodeBlock:
			html_file.write("\t\t<p class=\"code\">\n\t\t{}</p>\n".format(token.TokenValue[1].replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;").replace(" ", "&nbsp;").replace("\n", "<br/>\n\t\t")))
		elif token.TokenType == Token.TokenType.InlineCodeBlock:
			html_file.write("<span class=\"code\">{}</span>".format(token.TokenValue))

		elif token.TokenType == Token.TokenType.Image:
			html_file.write("\t\t<img src=\"{}\"/>".format(token.TokenValue))
		elif token.TokenType == Token.TokenType.Link:
			html_file.write("<a href=\"{}\">{}</a>".format(token.TokenValue[1], token.TokenValue[0]))

		elif token.TokenType == Token.TokenType.Text:
			if token.TokenValue == "\n" and i < len(scanner.Tokens) - 1 and scanner.Tokens[i + 1].TokenType == Token.TokenType.Text and scanner.Tokens[i + 1].TokenValue != "\n" and scanner.Tokens[i + 1].TokenValue != " " and scanner.Tokens[i + 1].TokenValue != "\t":
				html_file.write("\n\t\t")
			else:
				html_file.write(token.TokenValue)

		elif token.TokenType == Token.TokenType.BeginItalic:
			html_file.write("<i>")
		elif token.TokenType == Token.TokenType.EndItalic:
			html_file.write("</i>")

		elif token.TokenType == Token.TokenType.BeginBold:
			html_file.write("<b>")
		elif token.TokenType == Token.TokenType.EndBold:
			html_file.write("</b>")

		elif token.TokenType == Token.TokenType.BeginUnorderedList:
			html_file.write("\t\t<ul>\n")
		elif token.TokenType == Token.TokenType.EndUnorderedList:
			html_file.write("\n\t\t</ul>\n")
		elif token.TokenType == Token.TokenType.BeginUnorderedListItem:
			html_file.write("\t\t\t<li>")
		elif token.TokenType == Token.TokenType.EndUnorderedListItem:
			html_file.write("</li>")

	html_file.write("""\t\t<hr/>\n\t\tGenerated With CPU Instructions and <3 By <a href="https://github.com/OverShifted/Docy">Docy</a>\n\t</body>\n</html>""")

	md_file.close()
	html_file.close()

if __name__ == '__main__':
	main()
