from django import forms
from .authentication_form import AuthenticationForm

from .models import MembershipComments, SendMessage, Email, User


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['email']


class MembershipForm(forms.ModelForm):
    class Meta:
        model = MembershipComments
        fields = ['full_name', 'email', 'comment']



class SendMessag(forms.ModelForm):
    class Meta:
        model = SendMessage
        fields = ['full_name', 'email', 'message']


class LoginForm(AuthenticationForm):
    email = forms.EmailField()
    password = forms.CharField(max_length=255)


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField()
    password = forms.CharField(max_length=255)
    confirm_password = forms.CharField(max_length=255)

    def clean_email(self):
        email = self.data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Bunday {email} allaqachon mavjud')
        return email

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Password did not match')

        return password


class EmailForm(forms.Form):
    subject = forms.CharField(max_length=50)
    message = forms.CharField(widget=forms.Textarea)
    from_email = forms.EmailField()
    to = forms.EmailField()
