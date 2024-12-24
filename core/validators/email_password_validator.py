import re

def validate_length(passwd):
    """Check if password length is valid."""
    if len(passwd) < 6:
        raise ValueError('Password length should be at least 6 characters.')
    if len(passwd) > 20:
        raise ValueError('Password length should not be greater than 20 characters.')

def validate_character_types(passwd):
    """Check if password contains at least one digit, one uppercase letter, one lowercase letter, and one special symbol."""
    SpecialSym = ['$', '@', '#', '%']
    
    if not re.search(r'\d', passwd):  # Check for digit
        raise ValueError('Password should have at least one numeral.')
    if not re.search(r'[A-Z]', passwd):  # Check for uppercase letter
        raise ValueError('Password should have at least one uppercase letter.')
    if not re.search(r'[a-z]', passwd):  # Check for lowercase letter
        raise ValueError('Password should have at least one lowercase letter.')
    if not any(char in SpecialSym for char in passwd):  # Check for special symbol
        raise ValueError('Password should have at least one of the symbols $@#.')

def password_check(passwd):
    """Validate the given password based on length and character requirements."""
    validate_length(passwd)  # Validate password length
    validate_character_types(passwd)  # Validate character types

    return {'status': True, 'message': 'Password is valid.'}


def validate_email(email):
        """Validates email address format."""
        if not email.strip():
            raise ValueError('Please enter a valid email address.')

        regex = r'\b^(([^<>()\\.,;:\s@"]+(\.[^<>()\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$\b'
        if not re.fullmatch(regex, email):
            raise ValueError('Please enter a valid email address.')

        return None