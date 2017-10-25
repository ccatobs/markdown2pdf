
# Create latex template. The 'sed ...' command inserts the contents of
# header.latex after the 'for(...)' line. This is a hack to get around the
# fact that pandoc doesn't expand variables in snippets passed via the 
# --include-* options.
default.latex: header.latex
	pandoc --print-default-template=latex \
	    | sed -e '/\\tableofcontents/a \\\pagebreak' \
	    | sed -e '/for(header-includes)/r header.latex' -e 'x;$$G' \
	    > $@

