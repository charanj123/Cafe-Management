from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import userAccount

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username','gender', 'date_joined', 'last_login','is_admin', 'is_staff', 'phone_number','Address','user_DOB' )
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    
    
    
admin.site.register(userAccount, AccountAdmin)
