from ..utils.utils import TARGET_DIRECTORIES_I, TARGET_DIRECTORIES_II, WINDOWS_CREDENTIAL_LOCATIONS, HASH_KEYWORDS, HASH_REGEX
import os
import magic
import nltk
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Define specific file types and their characteristics
FILE_TYPES = {
    "executable": ["ELF", "PE32", "Mach-O"],
    "text": ["ASCII", "UTF-8", "Unicode"],
    "image": ["JPEG", "PNG", "GIF", "TIFF"],
    "document": ["PDF", "Microsoft Word", "OpenDocument"],
    "archive": ["ZIP", "RAR", "tar", "gzip"],
    "database": ["SQLite", "Berkeley DB", "MySQL"],
    "log": ["log file", "text"],
    "system": ["registry file", "system file", "configuration"]
}

# Expanded training data
training_data = [
    ("ELF 64-bit LSB executable, x86-64", "executable"),
    ("ASCII text", "text"),
    ("JPEG image data, JFIF standard 1.01", "image"),
    ("PDF document, version 1.5", "document"),
    ("Zip archive data", "archive"),
    ("SQLite 3.x database", "database"),
    ("ASCII text, with very long lines", "log"),
    ("Windows registry file, NT/2000 or above", "system"),
    # Add more examples for each file type
]

def extract_features(file_info):
    tokens = word_tokenize(file_info.lower())
    stop_words = set(stopwords.words('english'))
    return {word: True for word in tokens if word not in stop_words}

def train_classifier():
    training_set = [(extract_features(info), category) for (info, category) in training_data]
    return NaiveBayesClassifier.train(training_set)

def get_file_info(filepath):
    try:
        return magic.from_file(filepath)
    except:
        return "unknown"

def classify_file(classifier, filepath):
    file_info = get_file_info(filepath)
    features = extract_features(file_info)
    return classifier.classify(features)

def scan_system(classifier, start_path="/"):
    results = {category: [] for category in FILE_TYPES.keys()}
    results["unknown"] = []

    for root, _, files in os.walk(start_path):
        for file in files:
            filepath = os.path.join(root, file)
            category = classify_file(classifier, filepath)
            results[category].append(filepath)

    return results

if __name__ == "__main__":
    classifier = train_classifier()
    scan_results = scan_system(classifier, "/")  # Start from root, change as needed

    for category, files in scan_results.items():
        print(f"\n{category.upper()}:")
        for file in files[:10]:  # Print first 10 files in each category
            print(f"  {file}")
        if len(files) > 10:
            print(f"  ... and {len(files) - 10} more files")
