def is_customer(user):
    """Returns True if user belongs to Customers group"""
    
    if user.is_authenticated:
        if bool(user.groups.filter(name='Customers')):
            return True
    return False
