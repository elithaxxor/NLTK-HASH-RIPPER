# naive_bayes_classifier.py
import os
import re
import nltk
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

'''.	
    1.File Categories: Defined specific categories for stored hashes, log files, databases, SAM hive, and system files.
	2.	File Classification:
	    •  	First checks file names and extensions against predefined keywords for each category.
	    •	If not classified by name/extension, it analyzes the file content using the Naive Bayes classifier.
	3.	System Scanning: Added a `scan_system` function that recursively scans the file system, classifying each file it encounters.
	4.	Performance Optimization: Only reads the first 1KB of file content for classification to improve speed when dealing with large files.
	5.	Error Handling: Added try-except blocks to handle file access errors gracefully.
	6.	Results Organization: Organizes scan results by category for easy review.
'''

def download_nltk_resources():
    """
    Ensures that the required NLTK resources (punkt and stopwords) are downloaded.
    """
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)

# Define hash-related keywords and regex for file classification
HASH_KEYWORDS = ["hash", "ntlm", "md5", "sha1", "sha256", "bcrypt"]


# Download required NLTK resources (run once)
# nltk.download('punkt', quiet=True)
# nltk.download('stopwords', quiet=True)

# Define file categories and their characteristics
FILE_CATEGORIES = {
    "stored_hashes": ["hash", "ntlm", "md5", "sha1", "sha256", "bcrypt"],
    "log_files": ["log", "event", "syslog", "access.log", "error.log"],
    "databases": ["db", "sqlite", "mdf", "ldf", "accdb", "mdb"],
    "sam_hive": ["sam"],
    "system_files": ["system", "registry", "hklm"]
}

# Sample training data
training_data = [
    ("The password hash is stored in the SAM database", "stored_hashes"),
    ("Windows Event Log contains system activities", "log_files"),
    ("SQLite database file found in application data", "databases"),
    ("SAM hive contains user account information", "sam_hive"),
    ("System registry hive stores Windows configuration", "system_files"),
    ("MD5 hashes of user passwords detected", "stored_hashes"),
    ("Apache access logs show incoming requests", "log_files"),
    ("MySQL database files located in data directory", "databases"),
    ("SYSTEM hive contains driver and service info", "system_files"),
    ("NTLM hashes extracted from memory dump", "stored_hashes")
]

def extract_features(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    return {word: True for word in tokens if word not in stop_words}

def train_classifier():
    training_set = [(extract_features(text), category) for (text, category) in training_data]
    classifier = NaiveBayesClassifier.train(training_set)
    return classifier

def classify_file(classifier, filepath):
    try:
        # Check file extension and name first
        _, file_extension = os.path.splitext(filepath)
        file_name = os.path.basename(filepath).lower()

        for category, keywords in FILE_CATEGORIES.items():
            if any(keyword in file_name or keyword == file_extension[1:] for keyword in keywords):
                return category

        # If not classified by name/extension, analyze content
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read(1024)  # Read first 1KB to classify
            features = extract_features(content)
            return classifier.classify(features)
    except Exception as e:
        print(f"Error classifying file {filepath}: {e}")
        return "unknown"

def scan_system(classifier, start_path="/"):
    results = {category: [] for category in FILE_CATEGORIES.keys()}
    results["unknown"] = []

    for root, _, files in os.walk(start_path):
        for file in files:
            filepath = os.path.join(root, file)
            category = classify_file(classifier, filepath)
            results[category].append(filepath)

    return results

# Usage example
if __name__ == "__main__":
    # Ensure NLTK resources are available
    download_nltk_resources()
    classifier = train_classifier()
    scan_results = scan_system(classifier, "/")  # Start from root, change as needed

    for category, files in scan_results.items():
        print(f"\n{category.upper()}:")
        for file in files[:10]:  # Print first 10 files in each category
            print(f"  {file}")
        if len(files) > 10:
            print(f"  ... and {len(files) - 10} more files")
