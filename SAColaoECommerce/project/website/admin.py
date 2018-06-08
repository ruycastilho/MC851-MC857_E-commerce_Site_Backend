from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Client, Order, Product

# Register your models here.

admin.site.register(Client)
admin.site.register(Order)
admin.site.register(Product)

# # Define an inline admin descriptor for Employee model
# # which acts a bit like a singleton
# class ClientInline(admin.StackedInline):
#     model = Client
#     can_delete = True
#     verbose_name_plural = 'client'

# # Define a new User admin
# class UserAdmin(BaseUserAdmin):
#     inlines = (ClientInline, )

# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)