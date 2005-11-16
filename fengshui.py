#!/usr/bin/python

from optparse import OptionParser
import xml.dom.minidom
from rackbuilder import RackBuilder
import rack2cairo

def main():
	parser = OptionParser("usage: %prog [options] [filename]")
	parser.add_option("-T", "--type", dest="outputtype",
					  help="Write output in format TYPE", metavar="TYPE")
	parser.add_option("-o", "--output", dest="outfile",
					  help="Write output to file FILE", metavar="FILE")
	parser.add_option("-f", "--file", dest="infile",
					  help="Read input from file FILE", metavar="FILE")

	(options, args) = parser.parse_args()

	# guess stuff if options missing
	if not options.infile:
		try:
			options.infile = args[0]
		except IndexError:
			parser.error("incorrect number of arguments")
	if not options.outfile:
		o = sys.stdout
	else:
		o = open(options.outfile, "w")
	if not options.outputtype:
		options.outputtype = "png"

	ast = xml.dom.minidom.parse(options.infile)
	rack = RackBuilder().build(ast)
	rack2cairo.RackView(options.infile).render(rack, o)

	return 0

import sys

if __name__ == '__main__':
	r = main()
	sys.exit(r)
