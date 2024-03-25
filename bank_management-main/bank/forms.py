# forms.py
from django import forms
from .models import UserAccount

class UserAccountForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['user_id', 'email', 'name', 'balance', 'number', 'city', 'address', 'source', 'accountNo', 'branch', 'accountType']
