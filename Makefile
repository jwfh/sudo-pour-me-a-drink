.SUFFIXES: .tex .pdf .java .class
SHELL=		bash
CC=		clang
CFLAGS=		-g -Wall
JFLAGS= 	-g
JC= 		javac
JVM= 		java
BINARY= 		
CLASSES= 
TEX=		latexmk
TEXFLAGS=	-lualatex
TEXFILES= 	drinks.tex

all: $(BINARY) classes pdfs

classes: $(CLASSES:.java=.class)

pdfs: $(TEXFILES:.tex=.pdf)

.java.class:
	$(JC) $(JFLAGS) $*.java

.tex.pdf: $< .PHONY
	$(TEX) $(TEXFLAGS) $<

clean: .PHONY
	rm -f $(BINARY) $(CLASSES:.java=.class) $(foreach TEXFILE, $(TEXFILES), $(addprefix $(basename $(TEXFILE)), .log .out .fls .fdb_latexmk .aux .blg .idx .ind))

veryclean: clean
	rm -f *.pdf *.ps *.dvi *.dat

.PHONY:
