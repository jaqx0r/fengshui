#!/usr/bin/python

class SourcePosition:
    def __init__(self, linestart=0, linefinish=0, charstart=0, charfinish=0):
	self.linestart = linestart
	self.linefinish = linefinish
	self.charstart = charstart
	self.charfinish = charfinish

    def __str__(self):
	return "%d-%d:%d-%d" % (self.linestart, self.linefinish, self.charstart, self.charfinish)
	
if __name__ == '__main__':
    a = SourcePosition(linestart=1, charstart=1)
    print a
