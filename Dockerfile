FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
RUN apt-get update && \
    apt-get install -y \
        default-jre \
        git \
        graphviz \
        librsvg2-bin \
        pandoc \
        pandoc-citeproc \
        python3-pip \
        texlive-latex-extra \
        texlive-metapost \
        texlive-xetex

RUN pip3 install panflute==1.12

RUN git clone https://github.com/ccatp/markdown2pdf /opt/markdown2pdf

ENTRYPOINT ["/opt/markdown2pdf/markdown2pdf"]
