from account.models import User

class BasicUserSerializer():
    class Meta:
        model = User
        fields = ('id', 'email','name','phone','avatar','is_active')