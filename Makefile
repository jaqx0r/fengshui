%.ps: %.feng *.py
	python rackbuilder.py $< > $@

all: $(patsubst %.feng,%.ps,$(wildcard *.feng))

clean:
	-rm -f *.ps
