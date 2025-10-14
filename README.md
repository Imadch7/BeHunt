# BeHunt 🚀

## 📖 Desciption
BeHunt is an open-source web vulnerability analysis tool written in Python. it performs automated, non-intrusive enumeration and security testing of web applications. Its core functionality includes the automated detection of common weaknesses such as SQL Injection (SQLi) and Cross-Site Scripting (XSS) vulnerabilities. Then injecting payloads when said vulnerabilities are found.

## ✨ Features
- 🔍 Automated subdomain enumeration
- 🛡️ SQL Injection (SQLi) detection
- 🔐 Cross-Site Scripting (XSS) vulnerability scanning
- 📁 Local File Inclusion (LFI) testing
- 📊 Multiple output formats (TXT, JSON, HTML)
- 🎯 Custom payload wordlist support

## 🔧 Installation and setup

### 1️⃣ ⚙️ Clone the repo and navigate to the directory
```cmd
git clone https://github.com/Imadch7/BeHunt
cd behunt
```

### 2️⃣ 🐍 Install Python
Installing Python can be done from their official website [here](https://www.python.org/downloads/)
(Python version 3.12+)

### 3️⃣ 📦 Install the required libraries
```cmd
pip install -r requirements.txt
```

### 4️⃣ ▶️ Execute the alias script
```cmd
./alias.sh
```

### 5️⃣ 💽 Verify installation
```cmd
Behunt -h
```

##  Getting Started 
### Usage
```cmd
usage: Behunt [options]

options:
  -u URL, --url URL     Target HOST/URL
  -h, --help            Show this help message and exit
  -w WORDLIST, --wordlist WORDLIST
                        Payload wordlist
  -O {json,html,txt}, --output {json,html,txt}
                        Output format:
                         1. txt
                         2. json
                         3. html
  -E, --Enum            Enumerate all the subdomains of the URL
  -T {1,2,3}, --Tuning {1,2,3}
                        Tuning options:
                        [1]. LFI injection
                        [2]. SQLi (SQL injection)
                        [3]. XSS (Cross Site Scripting)
```

### Examples
- Basic vulnerability scan
```cmd
Behunt -u https://example.com
```

- Subdomain enumeration
```cmd
Behunt -u https://example.com -E
```

- SQL Injection testing with custom wordlist
```cmd
Behunt -u https://example.com -T 2 -w /path/to/wordlist.txt
```

- XSS scan with JSON output
```cmd
Behunt -u https://example.com -T 3 -O json
```