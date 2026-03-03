import re


def email_validation(email):
    gmail = re.compile(r".@gmail.com")
    if not gmail.findall(email):
        return False
    return True


def number_validation(phone: str):
    numbers = re.compile(r"/D")
    if numbers.findall(phone) and len(phone) != 9:
        return False
    return True


def is_valid_isbn13(isbn):
    # Remove hyphens and spaces
    clean_isbn = re.sub(r'[-\s]', '', isbn)

    # Must be exactly 13 digits
    if not (len(clean_isbn) == 13 and clean_isbn.isdigit()):
        return False

    # Calculate checksum
    # Weight: 1 for even index, 3 for odd index
    total = 0
    for i, digit in enumerate(clean_isbn):
        multiplier = 1 if i % 2 == 0 else 3
        total += int(digit) * multiplier

    # Valid if the total is divisible by 10
    return total % 10 == 0
