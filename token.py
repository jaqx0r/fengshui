#!/usr/bin/python

class Token:
	ID = 0
	RACK = 1
	SHELF = 2
	LCURLY = 4
	RCURLY = 5
	LSQUARE = 6
	RSQUARE = 7
	RACKARRAY = 8
	EQUALS = 9
	COMMA = 10
	SEMICOLON = 11
	STRINGLITERAL = 12
	EOF = 13
	INCLUDE = 14
	
	keywords = {
		'id': ID,
		'rack': RACK,
		'shelf': SHELF,
		'lcurly': LCURLY,
		'rcurly': RCURLY,
		'lsquare': LSQUARE,
		'rsquare': RSQUARE,
		'rackarray': RACKARRAY,
		'equals': EQUALS,
		'comma': COMMA,
		'semicolon': SEMICOLON,
		'eof': EOF,
		'include': INCLUDE
		}

	def __init__(self, kind, spelling, sourceposition):
		if kind is Token.EOF:
			self.kind = kind
			self.spelling = "eof"
			self.sourceposition = sourceposition
			return
		if kind == Token.ID:
			try:
				self.kind = self.keywords[spelling]
			except KeyError:
				self.kind = kind
		else:
			self.kind = kind
		self.spelling = spelling
		self.sourceposition = sourceposition

	def __str__(self):
		return "Kind = %d [%s], spelling = \"%s\", position = %s" % (self.kind, spell(self.kind), self.spelling, self.sourceposition)

def spell(kind):
	for spelling in Token.keywords:
		if Token.keywords[spelling] == kind:
			return spelling
	return None
