import argparse

parser = argparse.ArgumentParser(description='A test program.')

parser.add_argument("-p", "--print_string", help="Prints the supplied argument.", type=int)

args = parser.parse_args()

print(args.print_string)



for i in range(1000000):
    j = i
    print('fuck')