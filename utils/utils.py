import os, sys, time, re, magic, nltk, glob

def TARGET_DIRECTORIES():
    return [
        r"C:\Windows\System32\config",  # Location of SAM and SYSTEM files
        r"%SystemRoot%\WinSxS",         # Component Store for Windows files
        r"C:\Windows\Repair",
        r"C:\Windows\System32\config\SAM",
        r"C:\Windows\System32\config\SYSTEM",
        r"C:\Windows\System32\config\SECURITY",
        r"C:\Windows\System32\winevt\Logs",  # Event logs
        r"C:\Windows\debug",
        r"C:\Windows\Logs",
        r"%SystemRoot%\WinSxS",
        r"C:\Windows\Repair",
        r"C:\Users",  # User profiles
        r"C:\ProgramData",  # Application data
        r"C:\Windows\Prefetch",
        r"C:\Windows\Temp",
        r"C:\Users\*\AppData\Local\Temp",
        r"C:\Users\*\AppData\Roaming",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\WebCache",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\INetCache",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\History",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\UsrClass.dat",
        r"C:\Users\*\NTUSER.DAT",
        r"C:\Users\*\ntuser.ini",
        r"C:\Users\*\AppData\Local\Microsoft\Credentials",
        r"C:\Users\*\AppData\Roaming\Microsoft\Credentials",
        r"C:\Users\*\AppData\Local\Microsoft\Vault",
        r"C:\Users\*\AppData\Roaming\Microsoft\Protect",
        r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Cookies",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\Cookies",
        r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Recent",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\Recent",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer",
        r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\ThumbCache*",
        r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\ThumbCache*",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\IconCache*",
        r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\IconCache*",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.db",
        r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.db",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.log",
        r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.log",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.tmp",
        r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.tmp",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.dat",
        r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.dat",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.ini",
        r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.ini",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.txt",
        r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.txt",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.url",
        r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.url",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.lnk",
        r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.lnk",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.pf",
        r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.pf",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.reg",
        r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.reg",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.tmp",
        r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.tmp",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.dat",
        r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.dat",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.ini",
        r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.ini",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.txt",
        r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.txt",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.url",
        r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.url",
        r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.lnk",
        r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.lnk",# Backup SAM files
    ]



# Constants for Windows credential locations and hash patterns
def WINDOWS_CREDENTIAL_LOCATIONS():

    WINDOWS_CREDENTIAL_LOCATIONS = [
    r"C:\Windows\System32\config\SAM",
    r"C:\Windows\System32\config\SYSTEM",
    r"C:\Windows\System32\config\SECURITY",
    r"C:\Windows\System32\winevt\Logs",  # Event logs
    r"C:\Windows\debug",
    r"C:\Windows\Logs",
    r"%SystemRoot%\WinSxS",
    r"C:\Windows\Repair",
    r"C:\Users",  # User profiles
    r"C:\ProgramData",  # Application data
    r"C:\Windows\Prefetch",
    r"C:\Windows\Temp",
    r"C:\Users\*\AppData\Local\Temp",
    r"C:\Users\*\AppData\Roaming",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\WebCache",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\INetCache",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\History",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\UsrClass.dat",
    r"C:\Users\*\NTUSER.DAT",
    r"C:\Users\*\ntuser.ini",
    r"C:\Users\*\AppData\Local\Microsoft\Credentials",
    r"C:\Users\*\AppData\Roaming\Microsoft\Credentials",
    r"C:\Users\*\AppData\Local\Microsoft\Vault",
    r"C:\Users\*\AppData\Roaming\Microsoft\Protect",
    r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Cookies",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\Cookies",
    r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Recent",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\Recent",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer",
    r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\ThumbCache*",
    r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\ThumbCache*",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\IconCache*",
    r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\IconCache*",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.db",
    r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.db",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.log",
    r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.log",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.tmp",
    r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.tmp",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.dat",
    r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.dat",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.ini",
    r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.ini",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.txt",
    r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.txt",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.url",
    r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.url",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.lnk",
    r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.lnk",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.pf",
    r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.pf",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.reg",
    r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.reg",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.tmp",
    r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.tmp",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.dat",
    r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.dat",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.ini",
    r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.ini",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.txt",
    r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.txt",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.url",
    r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.url",
    r"C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\*.lnk",
    r"C:\Users\*\AppData\Roaming\Microsoft\Windows\Explorer\*.lnk",
]
    return WINDOWS_CREDENTIAL_LOCATIONS



def HASH_KEYWORDS():
    return [
        "hash", "ntlm", "lmhash", "mscach2", "sha1", "sha256", "md5"
    ]
def FILE_TYPES():
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
    return FILE_TYPES





# Define file categories and their characteristics
def FILE_CATEGORIES():

    return {
        "stored_hashes": ["hash", "ntlm", "md5", "sha1", "sha256", "bcrypt"],
        "log_files": ["log", "event", "syslog", "access.log", "error.log", "evtx"],
        "databases": ["db", "sqlite", "mdf", "ldf", "accdb", "mdb"],
        "sam_hive": ["sam"],
        "system_files": ["system", "registry", "hklm", "ini"],
        "credentials": ["password", "username", "login", "auth", "credential", "token"]
    }



def HASH_REGEX():
    return r'\b[a-fA-F0-9]{32}\b|\b[a-fA-F0-9]{40}\b|\b[a-fA-F0-9]{64}\b'


def scan_directories(directories):

    found_files = []
    for directory in directories:
        directory = os.path.expandvars(directory)

        # Check for wildcard characters in the directory path
        if '*' in directory:
            # Use glob to expand the wildcard pattern
            for expanded_path in glob.glob(directory):
                if os.path.exists(expanded_path):
                    for root, _, files in os.walk(expanded_path):
                        for file in files:
                            filepath = os.path.join(root, file)
                            found_files.append(filepath)
        else:
            if os.path.exists(directory):
                for root, _, files in os.walk(directory):
                    for file in files:
                        filepath = os.path.join(root, file)
                        found_files.append(filepath)
    return found_files