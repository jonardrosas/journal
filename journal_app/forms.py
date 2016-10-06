import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from models import Journal_entry, Journal


class RegistrationForm(forms.Form):
    first_name = forms.RegexField(regex=r'^[\w.@+-]+$',
                                  max_length=30,
                                  label=(""),
                                  error_messages={'invalid': _(
                                      "This value may contain only letters, numbers and @/./+/-/_ characters.")})
    last_name = forms.RegexField(regex=r'^[\w.@+-]+$',
                                 max_length=30,
                                 label=(""),
                                 error_messages={'invalid': _(
                                     "This value may contain only letters, numbers and @/./+/-/_ characters.")})
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), 
                label=(""),error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)),label=(""))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),label=(""))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), 
                label=(""))
 
    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))
 
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("Passwords did not match."))
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})
            self.fields['first_name'].widget.attrs.update({'placeholder': 'Firstname','ng-model': 'first_name'})
            self.fields['last_name'].widget.attrs.update({'placeholder': 'Lastname', 'ng-model': 'last_name'})
            self.fields['username'].widget.attrs.update({'placeholder':'Username','ng-model': 'username'})
            self.fields['email'].widget.attrs.update({'placeholder':'Email','ng-model': 'email'})
            self.fields['password1'].widget.attrs.update({'placeholder':'Password','ng-model': 'password1'})
            self.fields['password2'].widget.attrs.update({'placeholder':'Confirm password', 'ng-model': 'password2'})


class JournalEntryForm(forms.ModelForm):
    journal_id = forms.ModelChoiceField(queryset=Journal.objects.all(), label="Select Journal:")
    title = forms.CharField(widget=forms.TextInput, label='')
    description = forms.CharField(widget=forms.Textarea, label='')

    class Meta:
        model = Journal_entry
        fields = ('journal_id', 'title', 'description')


    def __init__(self, request, *args, **kwargs):
        super(JournalEntryForm, self).__init__(request, *args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})
            self.fields['journal_id'].queryset = Journal.objects.filter(created_by=1) #hardcoded the user need to change
            self.fields['title'].widget.attrs.update({'placeholder': 'Title'})
            self.fields['description'].widget.attrs.update({'placeholder':'Description'})

