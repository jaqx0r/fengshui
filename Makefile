%.ps: %.feng *.py
	python rackbuilder.py $< > $@

all: $(patsubst %.feng,%.ps,$(wildcard *.feng))
