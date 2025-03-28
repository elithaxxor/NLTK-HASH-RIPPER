import os
import re
import nltk
from nltk.classify import MultinomialNB
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline


''''
This script uses Multinomial Naive Bayes, which is particularly well-suited for text classification tasks. It's effective for our purpose because:
    •	It works well with discrete features (like word counts), which is ideal for analyzing file contents.
    •	It’s computationally efficient, allowing for quick scanning of many files.
    •	It can handle a large vocabulary of terms related to hashes, databases, logs, and credentials.
    3.	To improve the classifier's effectiveness for Windows systems:
        •	Add more Windows-specific training data, including examples of Windows registry files, SAM database content, and common Windows log formats.
    •	Include patterns for Windows file paths and system directories in the feature extraction process.
    •	Expand the `TARGET_FILES` dictionary with Windows-specific file extensions and keywords.
    4.	To enhance detection of hashes, passwords, and usernames:
    •	Implement regex patterns to identify common hash formats and credential patterns.
    •	Add a pre-processing step to extract potential credentials from configuration files.
    •	Include examples of encrypted password storage formats used in Windows (e.g., LM, NTLM hashes).
    5.	For better performance and accuracy:
    •	Use a larger training dataset with diverse examples of each file type.
    •	Implement cross-validation to tune the classifier’s hyperparameters.
    •	Consider using a combination of Multinomial Naive Bayes and other classifiers (like Decision Trees) in an ensemble for improved accuracy.

'''
nltk.download('punkt', quiet=True)

# Define target file types and their characteristics
TARGET_FILES = {
    "hashes": ["hash", "md5", "sha1", "sha256", "ntlm"],
    "databases": ["db", "mdf", "ldf", "accdb", "sqlite"],
    "log_files": ["log", "evt", "evtx"],
    "credentials": ["password", "username", "login", "auth"]
}

# Sample training data
training_data = [
    ("NTLM:4de7a8f35d37e7f8c32990af1f575f9e", "hashes"),
    ("SQLite format 3", "databases"),
    ("Windows Event Log", "log_files"),
    ("username=admin;password=secret123", "credentials"),
    # Add more examples for each category
]

def extract_features(text):
    return word_tokenize(text.lower())

def train_classifier():
    X, y = zip(*[(extract_features(text), category) for text, category in training_data])
    pipeline = Pipeline([
        ('vectorizer', CountVectorizer(tokenizer=lambda x: x, lowercase=False)),
        ('classifier', MultinomialNB())
    ])
    pipeline.fit(X, y)
    return pipeline

def classify_file(classifier, filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read(1024)  # Read first 1KB to classify
        return classifier.predict([extract_features(content)])[0]
    except Exception as e:
        print(f"Error classifying file {filepath}: {e}")
        return "unknown"

def scan_windows_system(classifier, start_path="C:\\"):
    results = {category: [] for category in TARGET_FILES.keys()}
    results["unknown"] = []

    for root, _, files in os.walk(start_path):
        for file in files:
            filepath = os.path.join(root, file)
            category = classify_file(classifier, filepath)
            results[category].append(filepath)

    return results

# Usage
if __name__ == "__main__":
    classifier = train_classifier()
    scan_results = scan_windows_system(classifier)

    for category, files in scan_results.items():
        print(f"\n{category.upper()}:")
        for file in files[:10]:  # Print first 10 files in each category
            print(f"  {file}")
        if len(files) > 10:
            print(f"  ... and {len(files) - 10} more files")
