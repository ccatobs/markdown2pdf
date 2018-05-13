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
        ofn = tempfile.mktemp(suffix='.pdf')
        args = ['dot',
                '-Earrowsize=0.6',
                '-Nfontname=dejavu sans,helvetica',
                '-Nfontsize=10',
                '-Nshape=rect',
                '-Tpdf',
                '-o', ofn]
        try:
            dot = subprocess.run(args,
                    input=elem.text.encode('utf8'),
                    stdout=subprocess.DEVNULL)
            if dot.returncode != 0:
                return
        except Exception as ex:
            err("error running dot")
            err(ex)

    elif 'plantuml' in elem.classes:
        if '@startuml' in elem.text:
            extra_args = ['-Smonochrome=true', '-Sshadowing=false']
        else:
            extra_args = []
        tmp = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
        txt = elem.text.encode('utf-8')
        if not txt.startswith(b"@start"):
            txt = b"@startuml\n" + txt + b"\n@enduml\n"             
        tmp.write(txt)
        tmp.close()
        #
        ifn = tmp.name
        ifn_without_ext = os.path.splitext(ifn)[0]
        iofn_svg = ifn_without_ext + '.svg'
        ofn = ifn_without_ext + '.pdf'
        jarsd = os.path.normpath(os.path.dirname(__file__) + '/../jars')
        args = ['java',
                '-cp', jarsd + '/*',
                'net.sourceforge.plantuml.Run',
                '-charset', 'UTF-8',
                '-tsvg',
                ifn] + extra_args
        err(" ".join(args))
        #
        plantuml = subprocess.check_call(args,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL)
        if plantuml != 0:
            return            
        # convert svg -> pdf
        args = ['rsvg-convert',
                '-f', 'pdf',
                '-o', ofn,
                iofn_svg]
        try:
            rsvg_convert = subprocess.run(args,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL)
            if rsvg_convert.returncode != 0:
                return
        except Exception as ex:
            err("error running rsvg-convert")
            err(ex)
        finally:
            os.unlink(iofn_svg)
    else:
        return

    img = panflute.Image(url=ofn)
    return panflute.Para(img)

def main(doc=None):
    panflute.run_filter(diagrams, doc=doc)

if __name__ == '__main__':
    try:
        import panflute
    except:
        err("can't import panflute")
        sys.stdout.write(sys.stdin.read())
    main()        

