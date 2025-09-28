import sys


def help():

	if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
    		print("Usage: python3 Behunt.py [options]")
    		print("Options:")
    		print("  -h, --help    Show this help message and exit.")
    		print("  -v            Enable verbose mode.")
    		sys.exit(0) 
	elif len(sys.argv) > 1 and sys.argv[1].startswith("-"):
		print("use: python3 Behunt.py -h")

if __name__ == "__main__":
	help()
