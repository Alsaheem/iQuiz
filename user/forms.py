from django import forms

from django.contrib.auth.models import User


from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):
    email = forms.CharField(required=True)
    username = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'last_name')
        def clean(self):
            cleaned_data=super(UserForm, self).clean()
            email = cleaned_data.get('email')
            username = cleaned_data.get('username')
            email_qs = User.objects.filter(email=email)
            username_qs = User.objects.filter(username=username)
            if email_qs.exists():
                raise ValueError('email exists, choose another!')
            return email_qs

            if username_qs.exists():
                raise ValueError('email exists, choose another!')
            return username_qs

            if not username and not email:
                raise forms.ValidationError('you have to write something')

