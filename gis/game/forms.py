from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    username = forms.CharField(
        label="Имя пользователя",
        min_length=3,
        max_length=30,
        error_messages={
            'required': 'Пожалуйста, введите имя пользователя',
            'unique': 'Это имя пользователя уже занято',
            'min_length': 'Имя пользователя должно содержать минимум 3 символа',
            'max_length': 'Имя пользователя должно содержать не более 30 символов',
            'invalid': 'Имя пользователя может содержать только буквы, цифры и символы @/./+/-/_'
        }
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Пожалуйста, введите пароль',
            'password_too_short': 'Пароль должен содержать минимум 8 символов',
            'password_too_common': 'Этот пароль слишком простой',
            'password_entirely_numeric': 'Пароль не может состоять только из цифр'
        }
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Пожалуйста, подтвердите пароль',
            'password_mismatch': 'Пароли не совпадают'
        }
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже зарегистрирован')
        return email

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Имя пользователя"
        self.fields['password'].label = "Пароль"
        
        # Переопределяем сообщения об ошибках
        self.error_messages['invalid_login'] = 'Неверное имя пользователя или пароль'
        self.error_messages['inactive'] = 'Этот аккаунт неактивен'

        # Можно также переопределить error_messages для конкретных полей, если необходимо
        self.fields['username'].error_messages.update({
            'required': 'Пожалуйста, введите имя пользователя',
            'invalid': 'Неверное имя пользователя или пароль'
        })
        self.fields['password'].error_messages.update({
            'required': 'Пожалуйста, введите пароль',
            'invalid': 'Неверное имя пользователя или пароль'
        })