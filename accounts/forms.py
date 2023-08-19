from django.forms import ModelForm
from .models import CustomUser, UserType
from django import forms
from django.contrib.auth.password_validation import validate_password


class PlaceholderMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_names = [field_name for field_name, _ in self.fields.items()]
        for field_name in field_names:
            field = self.fields.get(field_name)
            field.widget.attrs.update({'placeholder': field.label})


class SignupForm(PlaceholderMixin, ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ## SPECIFIC CLASS ##
        self.fields['email'].widget.attrs = {
            'placeholder': 'Email Address',
            'class': 'form-control'
        }
        self.fields['phone_number'].widget.attrs = {
            'placeholder': 'Phone Number',
            'class': 'form-control'
        }
        self.fields['password'].widget.attrs = {
            'placeholder': 'Enter Password',
            'class': 'form-control',
            'type': 'password',
        }

    attrs = {
        "type": "password"
    }
    password = forms.CharField(widget=forms.TextInput(attrs=attrs), validators=[validate_password])

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        retail = UserType.objects.filter(type='RETAIL')
        if retail.exists():
            user.user_type = retail.first()
        if commit:
            user.save()
        return user



    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'password')


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
