# Book Template repository

This book template repository is a default layout proposition for basic `epub` documents.

You may find [in this page](https://zedas.fr/activities/books/) a list of books I've made using this template.

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Wivik_book-template&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Wivik_book-template)

## How to use

The books are generated using the following default layout. By design, you can use several languages for your book.

```
.
├── book-en
│   ├── 00-01-title-page.md
│   ├── 00-02-preface.md
│   ├── 00-03-copyright-en.md
│   ├── 00-04-contributors.md
│   ├── 01-01-chapter-1.md
│   ├── 01-02-chapter-2.md
│   └── img
│       └── cc-by-sa.png
├── book-fr
│   ├── 00-01-title-page.md
│   ├── 00-02-preface.md
│   ├── 00-03-copyright-fr.md
│   ├── 00-04-contributors.md
│   ├── 01-01-chapter-1.md
│   ├── 01-02-chapter-2.md
│   └── img
│       └── cc-by-sa.png
```

### Title page

This file contains the book's metadata you should update.

```yaml

---
title: Your book title
author: Your author name
rights:  Creative Commons Attribution ShareAlike 4.0
language: en-US
cover-image: use the relative path from the repository root ex ./book-en/img/cover.jpg
description: You book description.
date: The publication date
---

```

### Preface

Not mandatory, you can remove it if you don't want to use it. You can also create on "introduction" file and some other usual books sections. The most important thing is to respect the file sorting.

### Copyright

This is where you can add the publication license of your work. By default I propose the CC-BY-SA 4.0.

### Contributors

Another example of book section you can use, or not. If you don't want to use it, delete the file.

### Content

This is your book content. Ensure they always have a page title or Pandoc may not separate the sections properly.

### Img folder

If your book contains images, this is where you can put them, including the cover.

Please note that the cover in the book metadata requires the full relative path from this repository root to work.

Otherwises, the images inside the book content only require to be linked using `img/the-image.png`.

## Generate your ebook

Once you're up to produce your ebook, you can use the `generate.sh` script.

This script will ask for some questions :

- Name of the file to create
- Book language to produce (fr or en according to the folder `book-xx`)
- Create the 1st chapter preview

Then, the `pandoc` command will be executed to produce the epub file.

Following that, the Python script `epub-quality-check` will be executed to verify if your ebook passed some quality gates, based on the metadata and the content, such as :

- The Title is not empty
- The Author is not empty
- The Description is not empty
- The ISBN13 is not empty and valid (the check digit will be calculated)
- The Book license is not empty
- The book date is not empty and a valid YYYY-MM-DD value
- The book is written in the declared language

## Contribute to the project

Fork the repository and propose a pull request.

If you've enjoyed this template, you may also support the project in the "Sponsor" section.

## License

The directory layout proposition and the generation script is licensed under MIT.

See [LICENSE](LICENSE.md) for more details.

This license does not cover the works produced with this repository.

Feel free to use whatever license you want for your work !
