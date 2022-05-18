from allauth.account import app_settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email, user_field

from django import forms
ACCOUNT_EMAIL_BLACKLIST = ["devaza.id", "mteen.net"]

class EmailAsUsernameAdapter(DefaultAccountAdapter):
    """
    Adapter that always sets the username equal to the user's email address.
    """

    def populate_username(self, request, user):
        # override the username population to always use the email
        user_field(user, app_settings.USER_MODEL_USERNAME_FIELD, user_email(user))

    def clean_email(self, email):
        domain = email.split('@')[1]
        if domain in ACCOUNT_EMAIL_BLACKLIST:
            raise forms.ValidationError(f"{domain} is a disposable email domain")
        return super().clean_email(email)


class NoNewUsersAccountAdapter(DefaultAccountAdapter):
    """
    Adapter that can be used to disable public sign-ups for your app.
    """

    def is_open_for_signup(self, request):
        # see https://stackoverflow.com/a/29799664/8207
        return False
