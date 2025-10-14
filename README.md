# BeHunt

![BeHunt Logo](img.png)

BeHunt is an open-source web vulnerability analysis tool written in Python. It performs automated, non-intrusive enumeration and security testing of web applications. Its core functionality includes the automated detection of common weaknesses such as SQL Injection (SQLi) and Cross-Site Scripting (XSS) vulnerabilities.

## Features

- 🔍 Automated subdomain enumeration
- 🛡️ SQL Injection (SQLi) detection
- 🔐 Cross-Site Scripting (XSS) vulnerability scanning
- 📁 Local File Inclusion (LFI) testing
- 📊 Multiple output formats (TXT, JSON, HTML)
- 🎯 Custom payload wordlist support

## Installation

Clone the repository:

```bash
git clone https://github.com/Imadch7/BeHunt.git
```

## Getting Started

1. Navigate to the BeHunt directory:
```bash
cd ~/BeHunt
```

2. Install all the requirments:
```bash
pip install -r requirements.txt
```


3. Execute the setup script:
```bash
echo "alias behunt='your dir/__init__.py'" >> ~/.zshrc ##OR ~/.bashrc
source ~/.zshrc ##OR ~/.bashrc
```

4. Verify installation:
```bash
behunt -h
```

## Usage

```
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

## Examples

### Basic vulnerability scan
```bash
Behunt -u https://example.com
```

### Subdomain enumeration
```bash
Behunt -u https://example.com -E
```

### SQL Injection testing with custom wordlist
```bash
Behunt -u https://example.com -T 2 -w /path/to/wordlist.txt
```

### XSS scan with JSON output
```bash
Behunt -u https://example.com -T 3 -O json
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open-source and available under the MIT License.

## Disclaimer

⚠️ **Important**: This tool is intended for educational purposes and authorized security testing only. Always obtain proper authorization before testing any web application. Unauthorized access to computer systems is illegal.

## Author

Created by [Imadch7](https://github.com/Imadch7)

## Repository

[https://github.com/Imadch7/BeHunt](https://github.com/Imadch7/BeHunt)
