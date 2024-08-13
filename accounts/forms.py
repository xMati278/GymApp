from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'id': 'login-username'
        })
    )
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-password'
        })
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'id': 'register-username'
        })
    )
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'register-password'
        })
    )
    retype_password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Retype Password',
            'id': 'retype-password'
        })
    )
    email = forms.EmailField(
        max_length=100,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
            'id': 'register-email'
        }))