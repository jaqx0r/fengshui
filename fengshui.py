#!/usr/bin/python

from optparse import OptionParser
import xml.dom.minidom
from rackbuilder import RackBuilder
import rack2cairo

def main():
	parser = OptionParser("usage: %prog [options] FILE")
	parser.add_option("-T", "--type", dest="outputtype",
					  help="Write output in format TYPE", metavar="TYPE")
	parser.add_option("-o", "--output", dest="outfile",
					  help="Write output to file FILE", metavar="FILE")

	(options, args) = parser.parse_args()

	# guess stuff if options missing
	if len(args) != 1:
		parser.error("incorrect number of arguments")
	infile = args[0]
	if not options.outfile:
		o = sys.stdout
	else:
		o = open(options.outfile, "w")
	if not options.outputtype:
		options.outputtype = "png"

	ast = xml.dom.minidom.parse(infile)
	rack = RackBuilder().build(ast)
	rack2cairo.RackView(infile).render(rack, o)

	return 0

import sys

if __name__ == '__main__':
	r = main()
	sys.exit(r)
