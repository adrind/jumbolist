from django.forms import ModelForm, TextInput, PasswordInput, CharField, RegexField, ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MyUserForm(ModelForm):
    email = CharField(label="", widget=TextInput(attrs={'placeholder': 'E-mail address'}))
    username = RegexField(label="", max_length=30, regex=r'^[\w.@+-]+$',
        help_text = "Please use letters, numbers, or @/./+/-/_",
        error_messages = {'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."},
        widget = TextInput(attrs={'placeholder': 'Username'}))
    password = CharField(label="", widget=PasswordInput(attrs={'placeholder':'Password'}))
    password2 = CharField(label="", widget=PasswordInput(attrs={'placeholder':'Re-type Password'}))

    class Meta:
        model=User
        fields = { 'email', 'username', 'password',}

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if not password2:
            raise ValidationError("You must confirm your password")
        if password1 != password2:
            print password1, password2
            raise ValidationError("Ahh Your passwords do not match")
        return password2

    def save(self, commit=True):
        user = super(MyUserForm, self).save(commit=False)
        user.set_password(self.clean_password2())
        if commit:
            user.save()
        return user



class MyUserCreationForm(UserCreationForm):
        def __init__(self, *args, **kwargs):
            super(MyUserCreationForm, self).__init__(*args, **kwargs)
            self.fields['username'].widget.attrs['placeholder'] = u'Username'
            self.fields['password'].widget.attrs['placeholder'] = u'Password'
            self.fields['email'].widget.attrs['placeholder'] = u'Email'

