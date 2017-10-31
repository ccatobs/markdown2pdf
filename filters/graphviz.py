#!/usr/bin/env python3

import subprocess
import sys
import tempfile

def err(msg):
    sys.stderr.write("markdown2pdf/filters/graphviz: {}\n".format(msg))

def graphviz(elem, doc):
    if type(elem) == panflute.CodeBlock and 'dot' in elem.classes:
        name = tempfile.mktemp(suffix='.pdf')
        args = ['dot', '-Tpdf', '-o', name]
        try:
            dot = subprocess.run(args, input=elem.text.encode('utf8'),
                    stdout=subprocess.DEVNULL)
            if dot.returncode == 0:
                img = panflute.Image(url=name)
                return panflute.Para(img)
        except:
            err("error running dot")

def main(doc=None):
    panflute.run_filter(graphviz, doc=doc)

if __name__ == '__main__':
    try:
        import panflute
        main()
    except:
        err("can't import panflute")
        sys.stdout.write(sys.stdin.read())

