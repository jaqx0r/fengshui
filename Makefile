%.png: %.svg
	convert svg:$< png:$@

%.ps: %.svg
	inkscape -z -f $< -p '> $@'

#all: racks.png racks.ps

racks.svg: $(wildcard *.py)
	python anchor.py
