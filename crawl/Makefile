

default: Files.make files

files:

Files.make: Makefile
	find . -name *.pdf | sed 's/\.pdf/\.txt/;s/^/files: /' > Files.make

.PHONY: default

-include Files.make


%.txt : %.pdf
	$(CURDIR)/../cite/FileConversionService/bin/extractText.pl $<
