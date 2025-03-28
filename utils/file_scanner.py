# file_scanner.py
import os
import re
from utils import HASH_KEYWORDS, HASH_REGEX
from NLTK_DUMPER.nltk_analyzer.nltk_analyzer import tokenize_and_filter

def scan_directories(directories):
    found_files = []
    for directory in directories:
        directory = os.path.expandvars(directory)  # Expand environment variables like %SystemRoot%
        if os.path.exists(directory):
            for root, _, files in os.walk(directory):
                for file in files:
                    filepath = os.path.join(root, file)
                    if is_relevant_file(filepath):
                        found_files.append(filepath)
    return found_files

def is_relevant_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
            # Tokenize and filter text using NLTK
            tokens_lower = tokenize_and_filter(content)

            # Check for hash-related keywords or hash patterns
            if any(keyword in tokens_lower for keyword in HASH_KEYWORDS) or re.search(HASH_REGEX, content):
                return True
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
    return False
