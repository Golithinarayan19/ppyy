def add(a, b=0):
    """
    Returns the sum of two numbers.
    Default value of b is 0.
    """
    return a + b


def subtract(a, b=0):
    """
    Returns the difference of two numbers.
    Default value of b is 0.
    """
    return a - b


def multiply(a, b=1):
    """
    Returns the product of two numbers.
    Default value of b is 1.
    """
    return a * b


def divide(a, b):
    """
    Returns the division of two numbers.
    Handles division by zero.
    """
    if b == 0:
        return "Error: Division by zero is not allowed"
    return a / b


def get_numbers():
    """
    Takes user input and returns two numbers.
    """
    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))
    return a, b


def calculator():
    """
    Main calculator logic based on user choice.
    """
    print("\nCalculator Menu")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")

    choice = input("Enter your choice (1/2/3/4): ")
    a, b = get_numbers()

    if choice == "1":
        print("Result:", add(a, b))
    elif choice == "2":
        print("Result:", subtract(a, b))
    elif choice == "3":
        print("Result:", multiply(a, b))
    elif choice == "4":
        print("Result:", divide(a, b))
    else:
        print("Invalid choice")


# Test functions independently
def test_functions():
    """
    Tests each calculator function independently.
    """
    print("\nTesting Functions")
    print("Add:", add(10, 5))
    print("Subtract:", subtract(10, 5))
    print("Multiply:", multiply(10, 5))
    print("Divide:", divide(10, 0))


# Program execution
if __name__ == "__main__":
    calculator()
    test_functions()
