import pygame as pg
import math


# Functions with one argument (binary_sequence)
def bin2dec(binary_sequence):
    if not all(char in '01' for char in binary_sequence):
        raise ValueError("Input must be a binary string (containing only '0' and '1').")
    return int(binary_sequence, 2)

def dec2bin(decimal_sequence):
    if not isinstance(decimal_sequence, int) or decimal_sequence < 0:
        raise ValueError("Input must be a non-negative integer.")
    return bin(decimal_sequence)[2:]

def main():

    print("Welcome to the Decimal-Binary Converter!")
    while True:
        print("\nPlease choose an option:")
        print("1. Convert Decimal to Binary")
        print("2. Convert Binary to Decimal")
        print("3. Exit")

        try:
            choice = int(input("Enter your choice (1/2/3): "))
            if choice == 1:
                # Decimal to Binary
                decimal_input = int(input("Enter a non-negative decimal number: "))
                binary_result = dec2bin(decimal_input)
                print(f"The binary representation of {decimal_input} is: {binary_result}")

            elif choice == 2:
                # Binary to Decimal
                binary_input = input("Enter a binary number (only 0s and 1s): ")
                decimal_result = bin2dec(binary_input)
                print(f"The decimal representation of {binary_input} is: {decimal_result}")

            elif choice == 3:
                # Exit the program
                print("Thank you for using the converter. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError as e:
            print(f"Error: {e}. Please try again.")

# Run the main function
if __name__ == "__main__":
    main()
