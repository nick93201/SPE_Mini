#!/usr/bin/python3
import math

def square_root(num):
    result = math.sqrt(num)
    print(result)
    return result

def factorial(num):
    result = math.factorial(num)
    print(result)
    return result

def natural_logarithm(num):
    result = math.log(num, math.e)
    print(result)
    return result

def power_function(base, exponent):
    result = math.pow(base, exponent)
    print(result)
    return result

def main():
    print("Choose an operation:")
    print("1. Square Root")
    print("2. Factorial")
    print("3. Natural Logarithm")
    print("4. Power Function")

    choice = int(input("Enter your choice (1/2/3/4): "))

    if choice == 1:
        num = float(input("Enter a number: "))
        square_root(num)
    elif choice == 2:
        num = int(input("Enter a number: "))
        factorial(num)
    elif choice == 3:
        num = float(input("Enter a number: "))
        natural_logarithm(num)
    elif choice == 4:
        base = float(input("Enter the base: "))
        exponent = float(input("Enter the exponent: "))
        power_function(base, exponent)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
