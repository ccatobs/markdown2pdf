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
```

Optionally, if you want to embed diagrams you'll need:

```
default-jdk
graphviz
python3-pip
```

and then run the command `$ pip3 install panflute`.

For [PlantUML](https://plantuml.com) diagrams, you'll need to download
the jar file and put it in the `jars/` subdirectory.
You'll also need the
[Batik](https://xmlgraphics.apache.org/batik/download.html)
jars in the same directory.
