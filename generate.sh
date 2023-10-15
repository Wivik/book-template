#!/usr/bin/env bash

# generate epub

DEFAULT_BASENAME=$(pwd | awk -F '/' '{print $NF}')
DEFAULT_LANG="fr"

read -p "Name of the epub file [ ${DEFAULT_BASENAME}] : " FILE_BASENAME
FILE_BASENAME=${FILE_BASENAME:-$DEFAULT_BASENAME}
echo "Available languages are : "
ls -d book*
read -p "Which language to use : [ ${DEFAULT_LANG} ] : " BOOK_LANG
BOOK_LANG=${BOOK_LANG:-$DEFAULT_LANG}
read -p "Review filename [ ${FILE_BASENAME}-${BOOK_LANG}.epub ] : " EPUB_FILE
EPUB_FILE=${EPUB_FILE:-"${FILE_BASENAME}-${BOOK_LANG}.epub"}
echo $EPUB_FILE

podman run --rm -v .:/workspace --workdir /workspace ghcr.io/wivik/pandoc-plantuml:latest -o ${EPUB_FILE} --filter=/filters/plantuml.py --resource-path=.:book-${BOOK_LANG} --standalone $(ls book-${BOOK_LANG}/00-*.md book-${BOOK_LANG}/01-*.md)


