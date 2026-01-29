import logging

# ----------------------------
# Logging Configuration
# ----------------------------
logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Application started")


# ----------------------------
# Sample Functions
# ----------------------------

def divide_numbers(a, b):
    try:
        logging.debug(f"Trying to divide {a} by {b}")
        result = a / b

    except ZeroDivisionError:
        logging.error("Division by zero attempted")
        print("Error: Cannot divide by zero")

    except TypeError:
        logging.error("Invalid data type used for division")
        print("Error: Please provide numeric values")

    else:
        logging.info("Division successful")
        print(f"Result: {result}")

    finally:
        logging.debug("Division operation completed")


def read_file(filename):
    try:
        logging.debug(f"Attempting to open file: {filename}")
        with open(filename, "r") as file:
            content = file.read()
            print(content)

    except FileNotFoundError:
        logging.error(f"File not found: {filename}")
        print("Error: File does not exist")

    except Exception as e:
        logging.exception("Unexpected error occurred")
        print("Unexpected error:", e)

    else:
        logging.info("File read successfully")

    finally:
        logging.debug("File operation finished")


# ----------------------------
# Simulating Runtime Errors
# ----------------------------

print("\n--- Division Tests ---")
divide_numbers(10, 2)
divide_numbers(5, 0)
divide_numbers(10, "a")

print("\n--- File Handling Tests ---")
read_file("sample.txt")
read_file("missing_file.txt")

