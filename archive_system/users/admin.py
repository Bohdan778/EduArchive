from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профілі'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_position', 'get_department')
    
    def get_position(self, obj):
        return obj.profile.position if hasattr(obj, 'profile') else ''
    get_position.short_description = 'Посада'
    
    def get_department(self, obj):
        return obj.profile.department if hasattr(obj, 'profile') else ''
    get_department.short_description = 'Відділ'

# Перереєстрація UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)