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
        if "filename" in elem.attributes:
            if not os.path.exists(os.path.dirname(elem.attributes["filename"])):
                os.makedirs(os.path.dirname(elem.attributes["filename"]))
            tmp = open(elem.attributes["filename"],'wb')
        else:
            tmp = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
        txt = elem.text.encode('utf-8')
        tmp.write(txt)
        tmp.close()
        #
        ifn = tmp.name
        ifn_without_ext = os.path.splitext(ifn)[0]
        iofn_svg = ifn_without_ext + '.svg'
        ofn = ifn_without_ext + '.pdf'
        if doc.format in ["odt","docx"]:
            ofn = iofn_svg
            export_type = "svg"
        else:
            export_type = "pdf"
        args = ['dot',
                '-Earrowsize=0.6',
                '-Nfontname=dejavu sans,helvetica',
                '-Nfontsize=10',
                '-Nshape=rect',
                '-T'+export_type, ifn,
                '-o', ofn]
        try:
            dot = subprocess.check_call(args)
            if dot != 0:
                err("error running dot")
                return
        except Exception as ex:
            err("error running dot")
            err(ex)

    elif 'plantuml' in elem.classes:
        if '@startuml' in elem.text:
            extra_args = ['-Smonochrome=true', '-Sshadowing=false']
        else:
            extra_args = []
        if "filename" in elem.attributes:
            if not os.path.exists(os.path.dirname(elem.attributes["filename"])):
                os.makedirs(os.path.dirname(elem.attributes["filename"]))
            tmp = open(elem.attributes["filename"],'wb')
        else:
            tmp = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
        #
        for attr in elem.attributes:
            # skin parameters (http://plantuml.com/skinparam) can be set from attributes
            # for example Smonochrome=false
            if attr[0]=="S":
                extra_args.append("-{0}={1}".format(attr,elem.attributes[attr]))
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
                '-jar', jarsd + '/plantuml.jar',
                '-charset', 'UTF-8',
                '-tsvg',
                ifn] + extra_args
        #err(" ".join(args))
        #
        plantuml = subprocess.check_call(args)
        if plantuml != 0:
            return
        if doc.format in ["odt","docx"]:
            ofn = iofn_svg
        else:
            # convert svg -> pdf
            args = ['rsvg-convert',
                    '-f', 'pdf',
                    '-o', ofn,
                    iofn_svg]
            rsvg_convert = subprocess.check_call(args,
                        stdin=subprocess.DEVNULL,
                        stdout=subprocess.DEVNULL)
    else:
        return
    #
    additional_attributes = []
    for key,value in elem.attributes.items():
        if key=='caption':
            additional_attributes.append(panflute.Str(value))
        elif key=='cross_ref':
            #
            additional_attributes.append(panflute.RawInline("\\label{{{0}}}".format(value), format="latex"))
    if "caption" in elem.attributes:
        img = panflute.Image(*additional_attributes,url=ofn, title="fig:")
    else:
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
