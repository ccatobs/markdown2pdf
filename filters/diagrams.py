#!/usr/bin/env python3

import os
import subprocess
import sys
import tempfile

def err(msg):
    sys.stderr.write("markdown2pdf/filters/diagrams: {}\n".format(msg))

def diagrams(elem, doc):
    if type(elem) != panflute.CodeBlock:
        return

    if 'dot' in elem.classes:
        name = tempfile.mktemp(suffix='.pdf')
        args = ['dot',
                '-Earrowsize=0.6',
                '-Nfontname=dejavu sans,helvetica',
                '-Nfontsize=10',
                '-Nshape=rect',
                '-Tpdf',
                '-o', name]
        try:
            dot = subprocess.run(args, input=elem.text.encode('utf8'),
                    stdout=subprocess.DEVNULL)
            if dot.returncode == 0:
                img = panflute.Image(url=name)
                return panflute.Para(img)
        except:
            err("error running dot")

    elif 'plantuml' in elem.classes:
        input = "@startuml\n" + elem.text + "\n@enduml"
        tmp = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
        tmp.write(input.encode('utf-8'))
        tmp.close()
        ifn = tmp.name
        ofn = os.path.splitext(ifn)[0] + '.pdf'
        jarsd = os.path.normpath(os.path.dirname(__file__) + '/../jars')
        args = ['java',
                '-cp', jarsd + '/*',
                'net.sourceforge.plantuml.Run',
                '-charset', 'UTF-8',
                '-Smonochrome=true',
                '-Sshadowing=false',
                '-tpdf',
                ifn]
        try:
            dot = subprocess.run(args,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL)
            if dot.returncode == 0:
                img = panflute.Image(url=ofn)
                return panflute.Para(img)
        except Exception as ex:
            err("error running plantuml")
            err(ex)
        finally:
            os.unlink(ifn)

def main(doc=None):
    panflute.run_filter(diagrams, doc=doc)

if __name__ == '__main__':
    try:
        import panflute
        main()
    except:
        err("can't import panflute")
        sys.stdout.write(sys.stdin.read())

