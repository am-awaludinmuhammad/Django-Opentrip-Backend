from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import User

class CustomUserAdmin(UserAdmin):
    model = User

    add_fieldsets = (
        (None, {
            'fields': ('email','password1','password2','name','phone','avatar','is_staff','is_active'),
        }),
    )

     # Specify the fields that should be displayed in the change user form
    fieldsets = (
        (None, {'fields': ('email', 'password','name', 'phone', 'avatar', 'is_staff', 'is_active',)}),
    )

    search_fields = ('email',)
    
    # Customize the list display as needed
    list_display = ('email','name', 'phone', 'avatar', 'is_staff', 'is_active')

    # Customize other admin options as needed
    ordering = ['email']  # Update this to a valid field of CustomUser model

admin.site.register(User, CustomUserAdmin)