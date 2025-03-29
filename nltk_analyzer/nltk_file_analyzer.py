import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import shutil

# Download required NLTK resources
nltk.download('wordnet')
nltk.download('stopwords')

# Define categories and keywords
categories = {
    "Network Scanning": ["nmap", "nessus", "openvas"],
    "Vulnerability Exploitation": ["metasploit", "exploitdb"],
    "Password Cracking": ["john", "hashcat", "rainbowcrack"],
    "Web Application Scanning": ["burpsuite", "zaproxy", "sqlmap"],
    "Miscellaneous": []  # Default category
}

# Initialize NLP tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def categorize_tool(tool_name):
    """
    Categorizes a given tool name based on defined categories and keywords.

    Parameters:
    tool_name (str): The name of the tool to categorize.

    Returns:
    str: The category to which the tool belongs.
    """
    # Tokenize tool name
    tokens = nltk.word_tokenize(tool_name)

    # Remove stop words and lemmatize tokens
    tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens if token.lower() not in stop_words]

    # Check for keyword matches
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in tokens:
                return category

    # Default to Miscellaneous category
    return "Miscellaneous"

def organize_tools(root_dir):
    """
    Organizes tools in the specified directory based on category.

    Parameters:
    root_dir (str): The path to the directory containing tools.
    """
    for tool in os.listdir(root_dir):
        tool_path = os.path.join(root_dir, tool)
        if os.path.isfile(tool_path):
            category = categorize_tool(tool)
            category_dir = os.path.join(root_dir, category)
            if not os.path.exists(category_dir):
                os.makedirs(category_dir)
            shutil.move(tool_path, category_dir)

    print("Tools organized!")

# Set the path to the tools
root_dir = "/path/to/your/tools"
organize_tools(root_dir)
