def is_client(user):
    """Returns True if user belongs to Clients group"""
    
    if user.is_authenticated:
        if bool(user.groups.filter(name='Clients')):
            return True
    return False
