#!/usr/bin/env python3

import os
import subprocess
import sys
import tempfile

def err(msg):
    sys.stderr.write("markdown2pdf/filters/diagrams: {}\n".format(msg))

def extract_code_to_tmpfile_with_ext(elem, ext):
    if ext.startswith('.'):
        suffix = ext
    else:
        suffix = '.' + ext
    tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    txt = elem.text.encode('utf-8')
    tmp.write(txt)
    tmp.close()
    return tmp

def diagrams(elem, doc):
    if type(elem) != panflute.CodeBlock:
        return
    if 'dot' in elem.classes:
        tmp = extract_code_to_tmpfile_with_ext(elem, 'dot')
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
                '-Efontname=dejavu sans,helvetica',
                '-Gfontname=dejavu sans,helvetica',
                '-Nfontname=dejavu sans,helvetica',
                '-Efontsize=9',
                '-Gfontsize=11',
                '-Nfontsize=10',
                '-Nshape=rect',
                '-T'+export_type, ifn,
                '-o', ofn]
        try:
            subprocess.check_call(args)
        except Exception as ex:
            err("error running dot")
            err(ex)
            return

    elif 'metapost' in elem.classes:
        f = extract_code_to_tmpfile_with_ext(elem, 'mp')
        ifn = f.name
        ofn = ifn[:-3] + '-1.pdf'
        try:
            subprocess.check_output(['mptopdf', ifn],
                    cwd=os.path.dirname(ifn),
                    stdin=subprocess.DEVNULL)
        except subprocess.CalledProcessError as ex:
            err("error running metapost")
            err(ex)
            err(ex.output)
            return

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

        try:
            subprocess.check_call(args)
        except Exception as ex:
            err("error running plantuml")
            err(ex)
            return

        if doc.format in ["odt","docx"]:
            ofn = iofn_svg
        else:
            # convert svg -> pdf
            args = ['rsvg-convert',
                    '-f', 'pdf',
                    '-o', ofn,
                    iofn_svg]
            subprocess.check_call(args,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL)
    else:
        return

    img_args = []
    img_opts = dict(url=ofn)
    for key,value in elem.attributes.items():
        if key == 'caption':
            img_args.append(panflute.Str(value))
            # strange, caption arg is ignored unless title is set
            img_opts['title'] = 'fig:'
        elif key == 'cross_ref':
            img_args.append(panflute.RawInline(
                "\\label{{{0}}}".format(value), format="latex"))
    img = panflute.Image(*img_args, **img_opts)
    return panflute.Para(img)

def main(doc=None):
    panflute.run_filter(diagrams, doc=doc)

if __name__ == '__main__':
    try:
        import panflute
    except Exception as ex:
        err(ex)
        sys.stdout.write(sys.stdin.read())
    main()
