from django.utils.translation import ugettext_lazy as _
from django import forms
from ..models import User

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("full_name",  "email",  "password", "terms", "username")

    password = forms.CharField(widget=forms.PasswordInput())
    
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(SignUpForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['full_name'].required = True
        self.fields['email'].required = True
        self.fields['password'].required = True
        self.fields['terms'].required = True
        self.fields['password'].label = _("Password")
        self.fields['username'].required = True
