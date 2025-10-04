import sys
from core import arg
from core import spider
from modules import docker_hakraw



if __name__ == "__main__":
	print("Welcome to Behunt")
	try:
		arg = arg.CLI()
		parser = arg.Arguments()
		if sys.argv[1] in ('-h', '--help'):
			print("Options:")
			print(parser.format_help())
			sys.exit(0)

		args = parser.parse_args()
		print(args.url)
		spi = docker_hakraw.Url_ENUM(args.url)
		spi.run()
	except IndexError as e:
		print("No arguments provided. Use -h or --help for usage information.")
		sys.exit(1)
	except Exception as e:
		print(f"An error occurred: {e}")
		sys.exit(1)
		
