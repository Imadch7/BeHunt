import argparse

class CLI:

    def __init__(self):
        pass


    def Arguments(self):
        parser = argparse.ArgumentParser(add_help=False,formatter_class=argparse.RawTextHelpFormatter,usage="python3 Behunt.py [options]")
        
        parser.add_argument("-h","--host",help="Target HOST/URL",action="store")

        parser.add_argument("-u","--url",help="Target HOST/URL",action="store",required=True)

        parser.add_argument("-v","--verbose",help="Enable verbose output",action="store_true")

        parser.add_argument("-D","--Display",help="Display all the modules",action="store_true")

        parser.add_argument("-F","--Format+",help="Output format:       \n 1. txt.\n 2.json.\n 3.xml.\n 4.csv.\n 5.sql )",choices=['1','2','3','4','5'],default='1')

        parser.add_argument("-ipv4","--ipv4",help="IPv4 Only",action="store_true")

        parser.add_argument("-ipv6","--ipv6",help="IPv6 Only",action="store_true")

        parser.add_argument("-mutate","--mutate",help="mutate options :\n 1. Guess for password file names.\n" \
                            "2.Enumerate user names via Apache (/~user type requests).\n" \
                            "3.Enumerate user names via cgiwrap (/cgi-bin/cgiwrap/~user type requests)",choices=['1','2','3'],default='1')

        parser.add_argument("-p","--port",help="Port to scan",type=int,default=80)

        parser.add_argument("-no404","--no404",help="Ignore 404 responses",action="store_true")

        parser.add_argument("-T","--Tuning",help="Tuning options:       \n" \
                            "1. Interesting Files.\n" \
                            "2. SQLi(SQL injection)\n" \
                            "3. XSS <Script,HTML>.\n" \
                            "4. Autentication Bypass.",choices=['1','2','3','4'],default='2')

        return parser