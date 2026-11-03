# utils.py
# This file contains helper functions for validation and formatting.

import re


def validate_email(email):
    """
    Validates email format: must be non-empty, contain '@' and '.',
    with valid characters and a domain extension with at least 2 letters.
    """
    if not email or not isinstance(email, str):
        return False
    email = email.strip()
    pattern = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_phone(phone):
    """
    Validates that a phone number is provided and contains exactly 10 digits.
    Handles empty input, strings, and accepts formatted or raw 10-digit numbers.
    """
    if not phone or not isinstance(phone, str):
        return False
    cleaned = phone.strip().replace("-", "").replace(" ", "")
    return cleaned.isdigit() and len(cleaned) == 10


def format_phone(phone):
    """
    Formats a 10-digit phone number into standard 'XXX-XXX-XXXX' format.
    """
    if not phone or not isinstance(phone, str):
        return ""
    cleaned = "".join(c for c in phone if c.isdigit())
    if len(cleaned) == 10:
        return f"{cleaned[:3]}-{cleaned[3:6]}-{cleaned[6:]}"
    return phone.strip()
