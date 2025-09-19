from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser,
    ContactUs,
    Product,
    Reviews,
    Checkout,
    Order,
    Payment,
    CartItem,
)

class CustomUserAdmin(UserAdmin):
    """
    Custom user admin.
    """
    model = CustomUser
    list_display = ('email', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'is_active')  # Replace 'is_staff' with 'is_admin'
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_admin', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ContactUs)
admin.site.register(Product)
admin.site.register(Reviews)
admin.site.register(Checkout)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Payment)