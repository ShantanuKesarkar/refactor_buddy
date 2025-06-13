def validate_user_data(data):
    if 'name' not in data or 'email' not in data:
        return (False, 'Name and email are required.')
    return (True, None)