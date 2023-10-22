#!/usr/bin/env bash


# The MIT License (MIT)

# Copyright (c) 2023 Seb

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# https://github.com/Wivik/book-template

# generate epub from repository

DEFAULT_BASENAME=$(pwd | awk -F '/' '{print $NF}')
DEFAULT_LANG="fr"
DEFAULT_OUTPUT_DIR="output"

if [ ! -d ${DEFAULT_OUTPUT_DIR} ]; then
    echo "📁 Creating output directory"
    mkdir ${DEFAULT_OUTPUT_DIR}
    if [ ! $? -eq 0 ]; then
        echo "😨 Couldn't create directory '${DEFAULT_OUTPUT_DIR}' !"
        exit 1
    else
        echo "👍 output directory '${DEFAULT_OUTPUT_DIR}' successfully created"
    fi
else
    echo "ℹ output directory '${DEFAULT_OUTPUT_DIR}' already exists"
fi


read -p "📕 Name of the epub file [ ${DEFAULT_BASENAME}] : " FILE_BASENAME
FILE_BASENAME=${FILE_BASENAME:-$DEFAULT_BASENAME}
echo "🌍 Available languages are : "
ls -d book*
read -p "Which language to use : [ ${DEFAULT_LANG} ] : " BOOK_LANG
BOOK_LANG=${BOOK_LANG:-$DEFAULT_LANG}
read -p "🔎 Review filename (⚠ existing files will be replaced ⚠) [ ${FILE_BASENAME}-${BOOK_LANG}.epub ] : " EPUB_FILE
EPUB_FILE=${EPUB_FILE:-"${FILE_BASENAME}-${BOOK_LANG}.epub"}

echo "⚙ Launch pandoc generator..."

podman run \
    --rm \
    -v .:/workspace \
    --workdir /workspace \
    ghcr.io/wivik/pandoc-plantuml:latest \
    -o ${DEFAULT_OUTPUT_DIR}/${EPUB_FILE} \
    --filter=/filters/plantuml.py \
    --resource-path=.:book-${BOOK_LANG} \
    --standalone $(ls book-${BOOK_LANG}/*.md)

if [ `ls ${DEFAULT_OUTPUT_DIR}/${EPUB_FILE}` ]; then
    echo "👏 File successfully created"
    ls ${DEFAULT_OUTPUT_DIR}/${EPUB_FILE}
else
    echo "😨 Couldn't find produced file, check output for error"
fi

