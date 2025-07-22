

import os
import argparse
from PyPDF2 import PdfReader
from transformers import pipeline
import torch
import re

def get_pdf_text(pdf_path):
    """Extracts text from all pages of a PDF."""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None

def get_info_from_text(text, question_answerer):
    """Uses a small LLM to find the title, authors, and year in the text."""
    if not text:
        return None
    try:
        # Ask for title, authors, and year in separate questions for better accuracy
        title_result = question_answerer(question="What is the title of the paper?", context=text)
        authors_result = question_answerer(question="Who are the authors of the paper?", context=text)
        year_result = question_answerer(question="What is the publication year of the paper?", context=text)

        return {
            'title': title_result['answer'],
            'authors': authors_result['answer'],
            'year': year_result['answer']
        }
    except Exception as e:
        print(f"Error getting info from text: {e}")
        return None

def extract_first_author(authors_text):
    """Extracts the first author from the text."""
    if not authors_text:
        return None
    # Split by common delimiters and take the first name
    authors = re.split(r',| and |\n', authors_text)
    return authors[0].strip()

def extract_year(year_text):
    """Extracts a 4-digit year from the text."""
    if not year_text:
        return None
    match = re.search(r'\b(\d{4})\b', year_text)
    return match.group(1) if match else None

def sanitize_filename_part(text):
    """Sanitizes the text to be a valid filename component."""
    if not text:
        return ""
    # Remove non-alphanumeric characters except spaces and underscores
    text = re.sub(r'[^\w\s_]', '', text)
    # Replace spaces with underscores
    return text.strip().replace(' ', '_')

def format_filename(year, first_author, title):
    """Formats the filename as year_first_author_title."""
    if not all([year, first_author, title]):
        return None
    
    sanitized_year = sanitize_filename_part(year)
    sanitized_author = sanitize_filename_part(first_author)
    sanitized_title = sanitize_filename_part(title)
    
    # Truncate title if it's too long
    if len(sanitized_title) > 50:
        sanitized_title = sanitized_title[:50]

    return f"{sanitized_year}_{sanitized_author}_{sanitized_title}.pdf"

def rename_pdfs(folder_path):
    """Renames all PDF files in a folder based on their title, author, and year."""
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        return

    # Initialize the pipeline once
    question_answerer = pipeline("question-answering", model="deepset/minilm-uncased-squad2")

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            old_path = os.path.join(folder_path, filename)
            print(f"Processing {old_path}...")

            text = get_pdf_text(old_path)
            if not text:
                print(f"  Could not extract text from {filename}. Skipping.")
                continue

            info = get_info_from_text(text, question_answerer)

            if info and all(info.values()):
                first_author = extract_first_author(info['authors'])
                year = extract_year(info['year'])
                new_filename = format_filename(year, first_author, info['title'])

                if new_filename:
                    new_path = os.path.join(folder_path, new_filename)

                    if not os.path.exists(new_path):
                        os.rename(old_path, new_path)
                        print(f"  Renamed to {new_path}")
                    else:
                        print(f"  Error: {new_path} already exists. Skipping.")
                else:
                    print(f"  Could not format a new filename for {filename}. Skipping.")
            else:
                print(f"  Could not determine all required info for {filename}. Skipping.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename PDF files based on their title, author, and year.")
    parser.add_argument("folder", help="The path to the folder containing PDF files.")
    args = parser.parse_args()

    rename_pdfs(args.folder)
