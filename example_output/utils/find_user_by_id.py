def find_user_by_id(user_id):
    for user in users:
        if user['id'] == user_id:
            return user
    return None