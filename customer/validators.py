from django.forms import ValidationError

def valid_phone_number(string):
    """Checks if a string is a valid phone number.
    
    Accepts two formats : only digits or '+' followed by digits ; otherwise raises a ValidationError"""
    if string[0] == '+':
        if not string[1:].isdigit():
            raise ValidationError('Not a valid phone number.')
    elif not string.isdigit():
        raise ValidationError('Not a valid phone number.')