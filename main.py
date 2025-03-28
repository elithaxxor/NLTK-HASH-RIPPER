# main.py
from NLTK_DUMPER.utils.utils import scan_directories, analyze_text_with_nltk
from NLTK_DUMPER.utils.utils import TARGET_DIRECTORIES
from NLTK_DUMPER.naive_bayes_classifyer.naive_bayes_classifier import train_classifier, classify_text

def main():
    print("Scanning Windows system for hashed files, text containing hashes, and databases...")

    # Train the Naive Bayes classifier
    classifier = train_classifier()

    # Step 1: Scan target directories
    print("Scanning target directories...")
    found_files = scan_directories(TARGET_DIRECTORIES)

    print("\nFiles containing potential hash-related content:")
    for file in found_files:
        print(file)
        analyze_text_with_nltk(file)

        # Classify the content of the file
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            category = classify_text(classifier, content)
            print(f"Classified as: {category}")

if __name__ == "__main__":
    main()
