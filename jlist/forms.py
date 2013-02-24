from django.forms import ModelForm, TextInput, PasswordInput, CharField, RegexField, ValidationError, DecimalField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from jlist.models import UserProfile, Item
from django.db import IntegrityError, models
from django import forms

class MyUserForm(ModelForm):
    email = RegexField(label="",
                      regex='r^[_a-z0-9-]+(\.[_a-z0-9-]+)+@tufts.edu',
                      widget=TextInput(attrs={'placeholder': 'Tufts e-mail address'}),
                      error_messages={'invalid' :"Need a valid Tufts e-mail"})
    username = RegexField(label="", max_length=30, regex=r'^[\w.@+-]+$',
        help_text = "Please use letters, numbers, or @/./+/-/_",
        error_messages = {'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."},
        widget = TextInput(attrs={'placeholder': 'Username'}))
    password = CharField(label="", widget=PasswordInput(attrs={'placeholder':'Password'}))
    password2 = CharField(label="", widget=PasswordInput(attrs={'placeholder':'Re-type Password'}))

    class Meta:
        model=UserProfile
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
        try:
            user = User.objects.create_user(self.cleaned_data['username'], self.cleaned_data['email'], self.clean_password2())
            user.save()
            #user = super(MyUserForm, self).save(commit=False)
            user_profile = UserProfile()
            user_profile.user = user
            user_profile.save()
            return user_profile
        except IntegrityError:
            raise ValidationError("Username already taken!")



class ItemForm(ModelForm):
    name = CharField(label="", widget=TextInput(attrs={'placeholder': 'Title'}))
    description = CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Description'}))
    price = DecimalField(label='',decimal_places=2, widget=TextInput(attrs={'placeholder': 'Price'}))
    photo = forms.FileField(label='')

    class Meta:
        model=Item
        fields = {'price', 'description', 'name', 'photo'}

    def save(self):
        item = Item()
        item.name = self.cleaned_data['name']
        item.description = self.cleaned_data['description']
        item.price = self.cleaned_data['price']
        item.sold = False
        #item.photo = self.cleaned_data
        #item.user = User.objects.get(user.username=)
        return item


class EmailForm(forms.Form):
    subject = forms.CharField(label='', max_length=100, widget=TextInput(attrs={'placeholder': 'Subject'}))
    message = forms.CharField(label='', widget=TextInput(attrs={'placeholder': 'Body'}))
    #sender = forms.EmailField(label='', widget=TextInput(attrs={'placeholder': 'Title'}))
    cc_me = forms.BooleanField(label='', required=False)
