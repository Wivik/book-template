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

from bs4 import BeautifulSoup
from datetime import datetime
from langcodes import Language
from langdetect import detect
import argparse
import ebooklib.epub
import sys

parser = argparse.ArgumentParser(description='Analyze epub file for quality issues.')
parser.add_argument('file', help='The epub file to analyze.')
args = parser.parse_args()

def extract_metadata(file):
    book = ebooklib.epub.read_epub(file, options={'ignore_ncx': True})

    isbn = [item[0] for item in book.get_metadata('DC', 'identifier')]
    title = [item[0] for item in book.get_metadata('DC', 'title')]
    author = [item[0] for item in book.get_metadata('DC', 'creator')]
    booklicense = [item[0] for item in book.get_metadata('DC', 'rights')]
    description = [item[0] for item in book.get_metadata('DC', 'description')]
    date = [item[0] for item in book.get_metadata('DC', 'date')]
    language = [item[0] for item in book.get_metadata('DC', 'language')]

    return isbn[0] if isbn else None, title[0] if title else None, author[0] if author else None, booklicense[0] if booklicense else None, description[0] if description else None, date[0] if date else None, language[0] if language else None

def extract_text_from_epub(file_path):
    book = ebooklib.epub.read_epub(file_path, options={'ignore_ncx': True})
    text_content = ''
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            text_content += item.get_content().decode('utf-8')
    return text_content

def check_date(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        print(f"⚠️ Date {date} is not using YYYY-MM-DD format.")
        return False

def check_language(epub_file, expected_language):
    # Remove the regional of the language code
    expected_language = expected_language[:2]
    # Extract the epub content
    extracted_text = extract_text_from_epub(epub_file)

    # Determine the language
    language_code = detect(extracted_text)

    # Use the name of the language instead of the ISO 639-1 code
    detected_language = Language.get(language_code)
    detected_language_name = detected_language.display_name()

    # Same for the expected language
    expected_language_complete_name = Language.get(expected_language)
    expected_language_name = expected_language_complete_name.display_name()

    print(f"ℹ️ The language detected for the book is: {detected_language_name} ({language_code})")
    if language_code != expected_language:
        print(f"⚠️ The text is assumed to be written in '{expected_language_name}' but the analyse determined it's {detected_language_name} ({language_code})")
        return False
    else:
        print(f"✅ The book is written in the expected {expected_language_name} language. Detected language : {detected_language_name} ({language_code})")
        return True

def check_isbn(isbn):
    # Remove any dashes and spaces
    isbn = isbn.replace('-', '').replace(' ', '')

    # Check if the ISBN is 13 digits long
    if len(isbn) != 13 or not isbn.isdigit():
        print(f"⚠️ The ISBN is not 13 digits long ({len(isbn)} detected) or contains invalid characters.")
        return False

    # Calculate the check digit
    total = sum(int(isbn[i]) * (3 if i % 2 else 1) for i in range(12))
    check_digit = 10 - (total % 10)
    if check_digit == 10:
        check_digit = 0

    # Compare it with the last digit
    return str(check_digit) == isbn[-1]

def check_data(item_to_check, value):
    if value is None:
        return False
    elif item_to_check == 'date':
        return check_date(value)
    elif item_to_check == 'language':
        return check_language(args.file, value)
    elif item_to_check == 'isbn':
        return check_isbn(isbn)
    else:
        return True


# Collect data
isbn, title, author, booklicense, description, date, language = extract_metadata(args.file)

# Storing variables and their corresponding check functions in a dictionary
data_to_check = [
    ("isbn", isbn),
    ("title", title),
    ("author", author),
    ("booklicense", booklicense),
    ("description", description),
    ("date", date),
    ("language", language)
]

# Initialize the counter for validation failures
failure_count = 0

print(f"Start to analyse {args.file}")

# Looping over the list and applying the validation
for data_type, value in data_to_check:
    if check_data(data_type, value):
        print(f"✅ {data_type} is provided and valid.")
    else:
        print(f"❌ {data_type} is missing or using an invalid format. Value : {value}.")
        failure_count += 1

# Pass the failure count as exit code
print(f"👓 Quality check completed with {failure_count} issue(s) detected.")
sys.exit(failure_count)
