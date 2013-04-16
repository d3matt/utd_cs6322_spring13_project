
ifeq ($(HIDE),)
HIDE:= @
endif

ifeq ($(shell ls ../perl/bin/perl 2>&1),../perl/bin/perl)
PERL := ../perl/bin/perl
else
PERL := /usr/bin/perl
endif

default: Files.make files

files:

Files.make: Makefile genFiles.sh
	./genFiles.sh

.PHONY: default

-include Files.make


%.txt : %.pdf
	@ echo "$< - extracting text"
	$(HIDE) $(PERL) $(CURDIR)/../cite/FileConversionService/bin/extractText.pl $< > /dev/null

%.check : %.txt
	@ echo "$< - checking"
	$(HIDE) $(PERL) $(CURDIR)/../cite/DocFilter/bin/filter.pl $< > $@

%.cxml : %.check
	$(HIDE) if [ "`cat $<`" != "document passed filtration" ] ; then \
		echo "`echo "$<" | sed 's/.check/.txt/'` failed validation...  not extracting citations" ;\
		echo "<notvalid />" > $@ ;\
	else \
		echo "`echo "$<" | sed 's/.check/.txt/'` - extracting citations" ;\
		$(PERL) $(CURDIR)/../cite/ParsCit/bin/citeExtract.pl `echo "$<" | sed 's/.check/.txt/'` | xmllint -format --output $@ - ; \
		rm -f `echo "$<" | sed 's/.check/.body/'` ; \
		rm -f `echo "$<" | sed 's/.check/.cite/'` ; \
	fi

%.hxml : %.check
	$(HIDE) if [ "`cat $<`" != "document passed filtration" ] ; then \
		echo "`echo "$<" | sed 's/.check/.txt/'` failed validation... not extracting headers" ;\
		echo "<notvalid />" > $@ ;\
	else \
		echo "`echo "$<" | sed 's/.check/.txt/'` - extracting header" ;\
		$(PERL) $(CURDIR)/../cite/HeaderParseService/bin/extractHeader.pl `echo "$<" | sed 's/.check/.txt/'` | xmllint -format --output $@ - ; \
	fi

clean:
	rm -f Files.make || true
	find . -name *.check -o -name *.txt -o -name *.cxml -o -name *.hxml -o -name *.cite -o -name *.body | xargs rm -v || true

#without this keywork, GNUmake deletes intermediate files
.SECONDARY:
