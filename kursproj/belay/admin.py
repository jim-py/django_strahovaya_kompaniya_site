from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *


class CustomUserAdmin(UserAdmin):
    readonly_fields = ['date_joined', 'last_login']
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Staff
    list_display = ['username', 'date_joined']


admin.site.register(Staff, CustomUserAdmin)
admin.site.register(Pact)
admin.site.register(Branch)
admin.site.register(TypePact)
admin.site.register(Client)
admin.site.register(Term)
admin.site.register(ClientEstate)
admin.site.register(StaffRole)
admin.site.register(StaffPost)
admin.site.register(News)
