from allauth.account.signals import user_signed_up, email_confirmed
from django.core.mail import mail_admins, send_mail
from django.dispatch import receiver

from apps.users.mailing_list import subscribe_to_mailing_list


@receiver(user_signed_up)
def handle_sign_up(request, user, **kwargs):
    # customize this function to do custom logic on sign up, e.g. send a welcome email
    # or subscribe them to your mailing list.
    # This example notifies the admins, in case you want to keep track of sign ups
    _notify_admins_of_signup(user)
    # and subscribes them to a mailchimp mailing list
    subscribe_to_mailing_list(user.email)
    send_mail("Welcome to Contaq.io!",
    '''Welcome to Contaq.io! We're so glad to have you on board.\n\nMy name is Mani and I built Contaq.io because the other lead gen platforms just didn't cut it.\n\nWho wants to use an outdated, unverified database, or a low-quality scraper that returns generic (info@business.com) emails?\n\nBut with Contaq.io, you'll be able to:\n\n - Scrape accurate contact info from businesses in real-time\n - Get the name, job title, LinkedIn, and email of decision makers (not info or support addresses)\n - Double-verify every email address\n - Access ANY city and ANY niche\n - Build lists of dozens of targeted, verified leads with one click\n\nFirst, you'll need to subscribe to get credits:\n\nhttps://contaq.io/subscriptions\n\nThen, you can start your first prospect search:\n\nhttps://contaq.io/search\n\nYou can type in any industry, location, and job title, then sit back while we scrape your list ;-)\n\n\nBest,\n\nMani Chadaga\nFounder\n\nP.S. If you have any questions about Contaq.io or need support, my direct line is mchadaga@college.harvard.edu or you can reach the support line at support@mg.contaq.io''',
     "Mani from Contaq.io <support@mg.contaq.io>", [user.email])




@receiver(email_confirmed)
def update_user_email(sender, request, email_address, **kwargs):
    """
    When an email address is confirmed make it the primary email.
    """
    # This also sets user.email to the new email address.
    # hat tip: https://stackoverflow.com/a/29661871/8207
    email_address.set_as_primary()


def _notify_admins_of_signup(user):
    mail_admins(
        "Yowsers, someone signed up for the site!",
        "Email: {}".format(user.email)
    )
