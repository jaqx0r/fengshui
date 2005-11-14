#!/usr/bin/python

import getopt
from rackbuilder import RackBuilder
import rack2cairo

import xml.dom.minidom

def usage():
	print "usage: %s -T type -o outfile -v view filename"

def main(args):
	try:
		opts, args = getopt.getopt(args, "T:o:v:f:", ["type=", "outfile=", "view=", "file="])
	except getopt.GetoptError, e:
		print e
		usage()
		return 1

	type = None
	outfile = None
	infile = None
	view = None

	for o, a in opts:
		if o == "-T":
			type = a
		elif o == "-o":
			outfile = a
		elif o == "-v":
			view = a
		elif o == "-f":
			infile = a

	# guess stuff if options missing
	if infile is None:
		try:
			infile = args[0]
		except IndexError:
			pass
	if outfile is None:
		o = sys.stdout
	else:
		o = open(outfile, "w")
	if type is None:
		type = "eps"

	ast = xml.dom.minidom.parse(infile)
	rack = RackBuilder().build(ast)
	rack2cairo.RackView(infile).render(rack, o)

import sys

if __name__ == '__main__':
	args = sys.argv[1:]
	r = main(args)
	sys.exit(r)
