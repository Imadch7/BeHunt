import sys
import 



if __name__ == "__main__":
	print("Welcome to Behunt")
	try:
		cli = CLI.CLI()
		parser = cli.Arguments()
		if sys.argv[1] in ('-h', '--help'):
			print("Usage: python3 Behunt.py [options]")
			print("Options:")
			print(parser.format_help())
			sys.exit(0)

		args = parser.parse_args()
		print(args.url)
		
	except IndexError as e:
		print("No arguments provided. Use -h or --help for usage information.")
		sys.exit(1)
	except Exception as e:
		print(f"An error occurred: {e}")
		sys.exit(1)
