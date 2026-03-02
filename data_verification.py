import re


def email_validation(email):
    gmail = re.compile(r".@gmail.com")
    if not gmail.findall(email):
        print("email is not valid")
        return False
    return True


def number_validation(phone):
    numbers = re.compile(r"/D")
    if numbers.findall(phone):
        print("Phone number is valid")
        return False
    return True


def isbn_validation(isbn):

    # 1. Clears the string (removes dashes and spaces)
    isbn = re.sub(r'[-\s]', '', isbn).upper()

    # 2. ISBN-10 Validation
    if len(isbn) == 10:
        if not re.match(r'^\d{9}[\dX]$', isbn):
            return False
        count = 0
        for i in range(10):
            val = 10 if isbn[i] == 'X' else int(isbn[i])
            count += val * (10 - i)
        return count % 11 == 0

    # 3. Validação ISBN-13
    elif len(isbn) == 13:
        if not isbn.isdigit():
            return False

        count = 0
        for i, digito in enumerate(isbn):
            # Alternating weights: 1 for even indices, 3 for odd indices.
            weights = 1 if i % 2 == 0 else 3
            count += int(digito) * weights
        return count % 10 == 0

    return False

