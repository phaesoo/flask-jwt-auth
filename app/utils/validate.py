import re
from string import ascii_letters, digits, punctuation, lowercase


__valid_username_chars = lowercase + digits
__valid_password_chars = ascii_letters + digits + punctuation


def check_username(username):
    is_valid = True
    err_msg = ""

    length = len(username)
    if length < 6:
        err_msg += "Length should be at least 6\n"
        is_valid = False
    if length > 20:
        err_msg += "Length should be not be greater than 20\n"
        is_valid = False

    has_invalid = False
    has_lower = False
    
    if username[0].isdigit():
        err_msg += "Should not have to start with digits\n"
        is_valid = False

    for char in username:
        if not has_invalid:
            if char not in __valid_username_chars:
                has_invalid = True
                continue
        if not has_lower:
            if char.islower():
                has_lower = True
                continue

    if has_invalid:
        err_msg += "Contains invalid character(Do not allows uppercase and special characters)\n"
        is_valid = False
    if not has_lower:
        err_msg += "Should have at least one lowercase letter\n"
        is_valid = False

    return is_valid, err_msg


def check_password(passwd):
    is_valid = True
    err_msg = ""

    length = len(passwd)
    if length < 6:
        err_msg += "Length should be at least 6\n"
        is_valid = False
    if length > 20:
        err_msg += "Length should be not be greater than 20\n"
        is_valid = False

    has_invalid = False
    has_digit = False
    has_upper = False
    has_lower = False
    has_symbol = False 
    
    for char in passwd:
        if not has_invalid:
            if char not in __valid_password_chars:
                has_invalid = True
                continue
        if not has_digit:
            if char.isdigit():
                has_digit = True
                continue
        if not has_upper:
            if char.isupper():
                has_upper = True
                continue
        if not has_lower:
            if char.islower():
                has_lower = True
                continue
        if not has_symbol:
            if char in punctuation:
                has_symbol = True
                continue

    if has_invalid:
        err_msg += "Contains invalid character\n"
        is_valid = False
    if not has_digit:
        err_msg += "Should have at least one digit\n"
        is_valid = False
    if not has_upper:
        err_msg += "Should have at least one uppercase letter\n"
        is_valid = False
    if not has_lower:
        err_msg += "Should have at least one lowercase letter\n"
        is_valid = False
    if not has_symbol:
        err_msg += "Should have at least one of the special symbols\n"
        is_valid = False
    
    return is_valid, err_msg


def check_email(adress):
    regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    if(re.search(regex, adress)):  
        return True, ""
    else:
        return False, "Invalid email adress"