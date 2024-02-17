#!/usr/bin/python3
import sys
import math

def square_root(num):
    return math.sqrt(num)

def factorial(num):
    return math.factorial(num)

def natural_logarithm(num):
    return math.log(num, math.e)

def power_function(base, exponent):
    return math.pow(base, exponent)

def main():
    if len(sys.argv) < 2:
        print("Usage: cal.py <operation> [arguments]")
        sys.exit(1)

    operation = sys.argv[1]

    if operation == 'sqrt':
        if len(sys.argv) < 3:
            print("Usage: cal.py sqrt <number>")
            sys.exit(1)
        num = float(sys.argv[2])
        square_root(num)
    elif operation == 'factorial':
        if len(sys.argv) < 3:
            print("Usage: cal.py factorial <number>")
            sys.exit(1)
        num = int(sys.argv[2])
        factorial(num)
    elif operation == 'log':
        if len(sys.argv) < 3:
            print("Usage: cal.py log <number>")
            sys.exit(1)
        num = float(sys.argv[2])
        natural_logarithm(num)
    elif operation == 'power':
        if len(sys.argv) < 4:
            print("Usage: cal.py power <base> <exponent>")
            sys.exit(1)
        base = float(sys.argv[2])
        exponent = float(sys.argv[3])
        power_function(base, exponent)
    else:
        print("Invalid operation:", operation)
        sys.exit(1)

if __name__ == "__main__":
    main()

