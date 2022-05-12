from django.core.mail import mail_admins
from djstripe import webhooks as djstripe_hooks
from djstripe.models import Customer, Subscription, Plan
from apps.users.models import CustomUser

from .helpers import provision_subscription

from apps.subscriptions.metadata import ACTIVE_PRODUCTS_BY_ID

@djstripe_hooks.handler("checkout.session.completed")
def checkout_session_completed(event, **kwargs):
    """
    This webhook is called when a customer signs up for a subscription via Stripe Checkout.

    We must then provision the subscription and assign it to the appropriate user/team.
    """
    session = event.data['object']
    client_reference_id = session.get('client_reference_id')
    subscription_id = session.get('subscription')

    subscription_holder = CustomUser.objects.get(id=client_reference_id)
    provision_subscription(subscription_holder, subscription_id)


@djstripe_hooks.handler("customer.subscription.updated")
def update_customer_plan(event, **kwargs):
    """
    This webhook is called when a customer updates their subscription via the Stripe
    billing portal.

    There are a few scenarios this can happen - if they are upgrading, downgrading
    cancelling (at the period end) or renewing after a cancellation.

    We update the subscription in place based on the possible fields, and
    these updates automatically trickle down to the user/team that holds the subscription.
    """
    # extract new plan and subscription ID
    new_plan = get_plan_data(event.data)
    subscription_id = get_subscription_id(event.data)

    # find associated subscription and change the plan details accordingly
    dj_subscription = Subscription.objects.get(id=subscription_id)
    dj_subscription.plan = Plan.objects.get(id=new_plan['id'])
    dj_subscription.cancel_at_period_end = get_cancel_at_period_end(event.data)
    dj_subscription.save()


@djstripe_hooks.handler('customer.subscription.deleted')
def email_admins_when_subscriptions_canceled(event, **kwargs):
    # example webhook handler to notify admins when a subscription is deleted/canceled
    try:
        customer_email = Customer.objects.get(id=event.data['object']['customer']).email
    except Customer.DoesNotExist:
        customer_email = 'unavailable'

    mail_admins(
        'Someone just canceled their subscription!',
        f'Their email was {customer_email}'
    )

@djstripe_hooks.handler('invoice.paid')
def give_user_credits(event, **kwargs):
    # example webhook handler to notify admins when a subscription is deleted/canceled
    # try:
    #     customer_email = Customer.objects.get(id=event.data['object']['customer']).email
    # except Customer.DoesNotExist:
    #     customer_email = 'unavailable'

    # mail_admins(
    #     'Someone just canceled their subscription!',
    #     f'Their email was {customer_email}'
    # )
    # print(event.data)
    subscription_id = event.data["object"]["subscription"]
    # print(subscription_id)
    user = CustomUser.objects.get(subscription__id=subscription_id)
    # print(user)
    prod_id = event.data["object"]["lines"]["data"][0]["plan"]["product"]
    credits = int(ACTIVE_PRODUCTS_BY_ID[prod_id].features[0][:-8])
    
    user.credits = user.credits + credits
    user.save()

@djstripe_hooks.handler('customer.subscription.deleted')
def cancel_subscription(event, **kwargs):
    subscription_id = event.data["object"]["subscription"]
    user = CustomUser.objects.get(subscription__id=subscription_id)

def get_plan_data(stripe_event_data):
    return stripe_event_data['object']['items']['data'][0]['plan']


def get_previous_plan_data(stripe_event_data):
    return stripe_event_data['previous_attributes']['items']['data'][0]['plan']


def get_subscription_id(stripe_event_data):
    return stripe_event_data['object']['items']['data'][0]['subscription']


def get_cancel_at_period_end(stripe_event_data):
    return stripe_event_data['object']['cancel_at_period_end']
