#!/usr/bin/env python3

import panflute
import subprocess
import tempfile

def graphviz(elem, doc):
    if type(elem) == panflute.CodeBlock and 'dot' in elem.classes:
        name = tempfile.mktemp(suffix='.pdf')
        args = ['dot', '-Tpdf', '-o', name]
        dot = subprocess.run(args, input=elem.text.encode('utf8'),
                stdout=subprocess.DEVNULL)
        if dot.returncode == 0:
            img = panflute.Image(url=name)
            return panflute.Para(img)

def main(doc=None):
    panflute.run_filter(graphviz, doc=doc)

if __name__ == '__main__':
    main()
