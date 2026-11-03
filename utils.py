# utils.py
# This file contains simple helper functions.


def validate_email(email):
    # Check that email has '@' and '.'
    if "@" in email and "." in email:
        return True
    return False


def validate_phone(phone):
    # Check that phone is numbers-only and exactly 10 digits
    if phone.isdigit() and len(phone) == 10:
        return True
    return False


def format_phone(phone):
    # Format '9876543210' into '987-654-3210'
    if len(phone) == 10:
        return phone[:3] + "-" + phone[3:6] + "-" + phone[6:]
    return phone
