import math

def square_root():
    num = float(input("Enter the number: "))
    result = math.sqrt(num)
    print("Square root of", num, "is:", result)

def factorial():
    num = int(input("Enter the number: "))
    result = math.factorial(num)
    print("Factorial of", num, "is:", result)

def natural_logarithm():
    num = float(input("Enter the number: "))
    result = math.log(num)
    print("Natural logarithm of", num, "is:", result)

def power_function():
    base = float(input("Enter the base: "))
    exponent = float(input("Enter the exponent: "))
    result = math.pow(base, exponent)
    print(base, "raised to the power", exponent, "is:", result)

def main():
    while True:
        print("\nScientific Calculator Menu:")
        print("1. Square root function - √x")
        print("2. Factorial function - x!")
        print("3. Natural logarithm (base е) - ln(x)")
        print("4. Power function - x power b")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            square_root()
        elif choice == '2':
            factorial()
        elif choice == '3':
            natural_logarithm()
        elif choice == '4':
            power_function()
        elif choice == '5':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")

if __name__ == "__main__":
    main()
