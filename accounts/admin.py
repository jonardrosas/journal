from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from accounts.models import UserProfile
from django.contrib.auth.models import User, Group

admin.site.unregister(User)
admin.site.unregister(Group)

class UserProfileAdmin(UserAdmin):
    list_display = ['first_name', 'last_name', 'username', 'email', 'password', 'get_text_password']
    #exclude = ['is_staff', 'is_active', 'date_joined', 'last_login', 'is_superuser', 'user_permissions', 'groups']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    def save_model(self, request, obj, form, change):
        obj.save()
        if form.cleaned_data.get('password1'):
            text_password = form.cleaned_data['password1']
            if hasattr(obj, 'profile'):
                obj.profile.text_password = password
                obj.save()
            else:
                UserProfile.objects.create(
                    user=obj,
                    text_password=text_password
                )

    def get_text_password(self, obj):
        return obj.profile.text_password
    get_text_password.short_description = 'Text Password'
    get_text_password.admin_order_field = 'profile__text_password'

# Register your models here.
admin.site.register(User, UserProfileAdmin)
