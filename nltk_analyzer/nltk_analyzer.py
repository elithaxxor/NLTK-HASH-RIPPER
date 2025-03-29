from ..utils.utils import TARGET_DIRECTORIES_I, TARGET_DIRECTORIES_II, WINDOWS_CREDENTIAL_LOCATIONS, HASH_KEYWORDS, HASH_REGEX
import os
import re
import platform
import subprocess
import json
import magic  # For file type detection
import csv
import shutil
from datetime import datetime

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure NLTK resources are downloaded
def download_nltk_resources():
    """Downloads required NLTK resources if not already present."""
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)

download_nltk_resources()

HASH_KEYWORDS = ["hash", "ntlm", "md5", "sha1", "sha256", "bcrypt", "lmhash"]
HASH_REGEX = r'\b[a-fA-F0-9]{32}\b|\b[a-fA-F0-9]{40}\b|\b[a-fA-F0-9]{64}\b'

# Define file categories and their characteristics
FILE_CATEGORIES = {
    "stored_hashes": ["hash", "ntlm", "md5", "sha1", "sha256", "bcrypt"],
    "log_files": ["log", "event", "syslog", "access.log", "error.log", "evtx"],
    "databases": ["db", "sqlite", "mdf", "ldf", "accdb", "mdb"],
    "sam_hive": ["sam"],
    "system_files": ["system", "registry", "hklm", "ini"],
    "credentials": ["password", "username", "login", "auth", "credential", "token"]
}

class WindowsCredentialScanner:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def tokenize_and_filter(self, text):
        tokens = word_tokenize(text)
        return [word.lower() for word in tokens if word.lower() not in self.stop_words]

    def is_relevant_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read(1024)  # Read first 1KB
                tokens_lower = self.tokenize_and_filter(content)

                if any(keyword in tokens_lower for keyword in HASH_KEYWORDS) or re.search(HASH_REGEX, content):
                    return True
                for category, keywords in FILE_CATEGORIES.items():
                    if any(keyword in tokens_lower for keyword in keywords):
                        return True
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
        return False

    def scan_directories(self, directories):
        found_files = []
        for directory in directories:
            directory = os.path.expandvars(directory)  # Expand environment variables like %SystemRoot%
            directory = directory.replace("*", "")
            if os.path.exists(directory):
                for root, _, files in os.walk(directory):
                    for file in files:
                        filepath = os.path.join(root, file)
                        if self.is_relevant_file(filepath):
                            found_files.append(filepath)
        return found_files

    def extract_metadata(self, filepath):
        """Extracts metadata from a file."""
        try:
            file_type = magic.from_file(filepath)
            file_size = os.path.getsize(filepath)
            creation_time = os.path.getctime(filepath)
            modification_time = os.path.getmtime(filepath)
            return {
                "file_type": file_type,
                "file_size": file_size,
                "creation_time": datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S'),
                "modification_time": datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S'),
            }
        except Exception as e:
            print(f"Error extracting metadata from '{filepath}': {e}")
            return {}

    def analyze_text_with_nltk(self, filepath):
        """Analyzes text content of a file using NLTK."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read(1024)  # Read first 1KB
                filtered_tokens = self.tokenize_and_filter(content)
                hashes_found = re.findall(HASH_REGEX, content)
                pos_tags = nltk.pos_tag(filtered_tokens)

                return {
                    "filtered_tokens": filtered_tokens[:10],
                    "hashes_found": hashes_found,
                    "pos_tags": pos_tags[:10]
                }
        except Exception as e:
            print(f"Error analyzing file {filepath}: {e}")
            return {}

    def scan_and_analyze(self, directories):
        """Scans directories, analyzes files, and extracts metadata."""
        found_files = self.scan_directories(directories)
        analysis_results = {}

        for filepath in found_files:
            metadata = self.extract_metadata(filepath)
            nltk_analysis = self.analyze_text_with_nltk(filepath)
            analysis_results[filepath] = {
                "metadata": metadata,
                "nltk_analysis": nltk_analysis
            }
        return analysis_results

    def generate_report(self, analysis_results, report_filename="credential_scan_report.json"):
        """Generates a report of the file analysis and saves it to a JSON file."""
        try:
            with open(report_filename, 'w') as f:
                json.dump(analysis_results, f, indent=4)
            print(f"Analysis report saved to '{report_filename}'.")
        except Exception as e:
            print(f"Error generating analysis report: {e}")

def main():
    scanner = WindowsCredentialScanner()
    analysis_results = scanner.scan_and_analyze(WINDOWS_CREDENTIAL_LOCATIONS)
    scanner.generate_report(analysis_results)

if __name__ == "__main__":
    main()


def tokenize_and_filter():
    pass
