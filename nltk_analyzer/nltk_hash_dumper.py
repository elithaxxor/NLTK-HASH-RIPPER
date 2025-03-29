import os
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Import from utils.py
from utils.utils import TARGET_DIRECTORIES, HASH_KEYWORDS, HASH_REGEX

# Download required NLTK resources (run once)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)


# Function to scan directories for specific files
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

# Function to check if a file contains relevant content
def is_relevant_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
            # Tokenize text using NLTK
            tokens = word_tokenize(content)
            tokens_lower = [token.lower() for token in tokens]

            # Check for hash-related keywords or hash patterns
            if any(keyword in tokens_lower for keyword in HASH_KEYWORDS()) or re.search(HASH_REGEX(), content):
                return True
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
    return False

# Function to analyze text files using NLTK
def analyze_text_with_nltk(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()

            # Tokenize text and remove stopwords
            tokens = word_tokenize(content)
            stop_words = set(stopwords.words('english'))
            filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

            # Extract potential hashes using regex
            hashes_found = re.findall(HASH_REGEX(), content)

            print(f"\nAnalysis of {filepath}:")
            print(f"Filtered Tokens: {filtered_tokens[:10]}...")  # Display first 10 tokens
            print(f"Hashes Found: {hashes_found}")
    except Exception as e:
        print(f"Error analyzing file {filepath}: {e}")

# Main function
def main():
    print("Scanning Windows system for hashed files, text containing hashes, and databases...")

    # Step 1: Scan target directories
    print("Scanning target directories...")
    found_files = scan_directories(TARGET_DIRECTORIES())

    print("\nFiles containing potential hash-related content:")
    for file in found_files:
        print(file)
        analyze_text_with_nltk(file)

if __name__ == "__main__":
    main()
