from bs4 import BeautifulSoup
import argparse
import ebooklib.epub
import json
import nltk
import yaml

# download nltk dictionnary
nltk.download('punkt', quiet=True)

parser = argparse.ArgumentParser(description='Count words and estimate pages in an epub file.')
parser.add_argument('file', help='The epub file to analyze.')
parser.add_argument('--words_per_page', type=int, default=280, help='The number of words per page for the page estimate. Default is 280 for fiction works. Non-fiction works can be set to 230.')
parser.add_argument('--output_format', choices=['text', 'json', 'yaml'], default='text', help='The output format. Can be "text", "json", or "yaml". Default is "text".')
args = parser.parse_args()

def count_words_and_pages(file, words_per_page):
    book = ebooklib.epub.read_epub(file, options={'ignore_ncx': True})
    total_words = 0

    for item in book.get_items():
        if isinstance(item, ebooklib.epub.EpubHtml):
            soup = BeautifulSoup(item.content, 'html.parser')
            text = soup.get_text()
            words = nltk.word_tokenize(text)
            total_words += len(words)

    # Estimate pages
    total_pages = total_words / words_per_page

    return total_words, round(total_pages)

def extract_metadata(file):
    book = ebooklib.epub.read_epub(file, options={'ignore_ncx': True})

    isbn = [item[0] for item in book.get_metadata('DC', 'identifier')]
    title = [item[0] for item in book.get_metadata('DC', 'title')]
    author = [item[0] for item in book.get_metadata('DC', 'creator')]
    booklicense = [item[0] for item in book.get_metadata('DC', 'rights')]
    description = [item[0] for item in book.get_metadata('DC', 'description')]

    return isbn[0] if isbn else None, title[0] if title else None, author[0] if author else None, booklicense[0] if booklicense else None, description[0] if description else None

# Collect data
words, pages = count_words_and_pages(args.file, args.words_per_page)
isbn, title, author, booklicense, description = extract_metadata(args.file)

# Render output
if args.output_format == 'text':
    print(f'Title: {title}')
    print(f'Author: {author}')
    print(f'ISBN: {isbn}')
    print(f'License: {booklicense}')
    print(f'Description: {description}')
    print(f'Total words: {words}')
    print(f'Total pages: {pages}')
elif args.output_format == 'json':
    print(json.dumps(
        {
            'title': title,
            'author': author,
            'isbn': isbn,
            'license': booklicense,
            'description': description,
            'total_words': words,
            'total_pages': pages
        }, ensure_ascii=False
    ))
elif args.output_format == 'yaml':
    print(yaml.dump(        
        {
            'title': title,
            'author': author,
            'isbn': isbn,
            'license': booklicense,
            'description': description,
            'total_words': words,
            'total_pages': pages
        }, allow_unicode=True
    ))
