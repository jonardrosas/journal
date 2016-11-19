from django.contrib import admin
import pdb
from django import forms
from django.contrib.auth.admin import UserAdmin
from accounts.models import UserProfile
from django.contrib.auth.models import User, Group, Permission

admin.site.unregister(User)
admin.site.unregister(Group)


class UserProfileAdmin(UserAdmin):
    list_display = ['first_name', 'last_name', 'username', 'email', 'get_signup_type', 'password', 'get_text_password']
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
        (('Permissions'), {'fields': ('is_active', 'is_staff',)}),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        if request.user.is_superuser:
            return (
                (None, {'fields': ('username', 'password')}),
                (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
                (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
            )
        else:
            return super(UserProfileAdmin, self).get_fieldsets(request, obj)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ['first_name', 'last_name', 'username', 'email', 'get_signup_type', 'password', 'get_text_password']
        else:
            return ['first_name', 'last_name', 'username', 'email', 'get_signup_type']

    def response_change(self, request, obj):
        print "this is a response change"
        if obj.is_staff:
            print "hes a staff"
            list_of_permission = [
                'add_journal', 'change_journal', 'delete_journal',
                'add_journal_entry', 'change_journal_entry', 'delete_journal_entry',
                'add_userprofile', 'change_userprofile', 'delete_userprofile',
                'add_user', 'change_user', 'delete_user']
            permission = Permission.objects.filter(codename__in=list_of_permission)
            for p in permission:
                obj.user_permissions.add(p)

        return super(UserProfileAdmin, self).response_change(request, obj)

    def save_model(self, request, obj, form, change):
        print obj
        obj.save()
        if form.cleaned_data.get('password1'):
            text_password = form.cleaned_data['password1']
            if hasattr(obj, 'profile'):
                obj.profile.text_password = text_password
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

    def get_signup_type(self, obj):
        return obj.profile.signup_type
    get_signup_type.short_description = 'Signup Type'
    get_signup_type.admin_order_field = 'profile__signup_type'

# Register your models here.
admin.site.register(User, UserProfileAdmin)
