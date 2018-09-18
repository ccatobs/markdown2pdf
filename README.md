# markdown2pdf

Usage:

```sh
./markdown2pdf filename.md
```

## Requirements

*Note: these are provided by the ['ccatp-dev' vagrant image](https://github.com/ccatp/os-images).*

On Ubuntu 18.04 LTS, the following packages are required:

```
pandoc
texlive-xetex
pandoc-citeproc
```

Optionally, if you want to embed diagrams you'll need:

```
default-jre
graphviz
librsvg2-bin
python3-pip
```

and then run the command `$ pip3 install panflute`.

For [PlantUML](https://plantuml.com) diagrams, you'll need to download
the jar file and put it in the `jars/` subdirectory.

For [latex support](http://plantuml.com/ascii-math) in plantuml you should add the following jars to your 
ext 
```
jlatexmath-1.0.3.jar
batik-all-1.10.jar
```


