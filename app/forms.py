from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    company = forms.CharField(max_length=50, required=True, label="Наименование компании")
    inn = forms.CharField(max_length=30, required=True, label="ИНН")
    first_name = forms.CharField(max_length=30, required=True, label="Имя")
    last_name = forms.CharField(max_length=30, required=True, label="Фамилия")
    phone = forms.CharField(max_length=30, required=True, label="Телефон")
    email = forms.EmailField(max_length=254, required=True, label="Email")
    agreement = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('company',
                  'inn',
                  'first_name',
                  'last_name',
                  'phone',
                  'email',
                  'username',
                  'password1',
                  'password2',
                  'agreement')


    def clean_agreement(self):
        agreement = self.cleaned_data['agreement']
        if not agreement:
            raise ValidationError("Необходимо принять условия договора-оферты")
        return agreement


