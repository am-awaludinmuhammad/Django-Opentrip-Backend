def user_is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)