import json

import djstripe
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import mail_admins, send_mail
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.subscriptions.helpers import get_stripe_module
from apps.subscriptions.metadata import get_product_and_metadata_for_subscription
from apps.utils.decorators import catch_stripe_errors


@login_required
@require_POST
@catch_stripe_errors
@transaction.atomic
def create_customer(request, subscription_holder=None):
    """
    Create a Stripe Customer and Subscription object and map them onto the subscription_holder

    Expects the inbound POST data to look something like this:
    {
        'email': 'cory@example.com',
        'userId': '23',
        'payment_method': 'pm_1GGgZaIYTEadrA0y0tthZ5UH'
    }
    """
    subscription_holder = subscription_holder if subscription_holder else request.user
    request_body = json.loads(request.body.decode('utf-8'))
    user_id = int(request_body['user_id'])
    email = request_body['user_email']
    assert request.user.id == user_id
    assert request.user.email == email

    

    payment_method = request_body['payment_method']
    plan_id = request_body['plan_id']
    stripe = get_stripe_module()

    # first sync payment method to local DB to workaround https://github.com/dj-stripe/dj-stripe/issues/1125
    payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
    djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)

    # create customer objects
    # This creates a new Customer in stripe and attaches the default PaymentMethod in one API call.
    customer = stripe.Customer.create(
      payment_method=payment_method,
      email=email,
      invoice_settings={
        'default_payment_method': payment_method,
      },
    )

    # create the local customer object in the DB so the subscription can use it
    djstripe.models.Customer.sync_from_stripe_data(customer)

    # create subscription
    subscription = stripe.Subscription.create(
      customer=customer.id,
      items=[
        {
          'plan': plan_id,
        },
      ],
      expand=['latest_invoice.payment_intent', 'pending_setup_intent'],
    )
    djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(subscription)

    # set subscription object on the subscription holder
    subscription_holder.subscription = djstripe_subscription
    subscription_holder.save()

    data = {
        'customer': customer,
        'subscription': subscription
    }
    return JsonResponse(
        data=data,
    )


@login_required
def subscription_success(request):
    return _subscription_success(request, request.user)


def _subscription_success(request, subscription_holder):
    if not subscription_holder.has_active_subscription():
        subscription = subscription_holder.subscription
        if not subscription:
            messages.error(
                request,
               "Oops, it looks like there was a problem processing your payment. "
               "Please try again, or get in touch if you think this is a mistake."
            )
        else:
            # 3D-Secure workflow hopefully completed successfully,
            # re-sync the subscription and hopefully it will be active
            subscription.sync_from_stripe_data(subscription.api_retrieve())

    if subscription_holder.has_active_subscription():
        subscription_name = get_product_and_metadata_for_subscription(
            subscription_holder.active_stripe_subscription
        ).metadata.name
        credits = get_product_and_metadata_for_subscription(
            subscription_holder.active_stripe_subscription
        ).metadata.features[0]
        messages.success(request, f"You've successfully signed up for {subscription_name}!\n"
                                  "Refresh to view your new credit balance.")
        # notify admins when someone signs up
        mail_admins(
            subject=f"Hooray! Someone just signed up for a {subscription_name} subscription!",
            message="Email: {}".format(request.user.email),
            fail_silently=True,
        )
        send_mail(f"You've signed up for a {subscription_name} subscription",
        f'''You've just signed up for the {subscription_name} subscription at Contaq.io. Great choice!\n\nThis subscription gets you {credits} per month. 1 credit = 1 verified email.\n\nReady to build your first lead list using Contaq.io?\n\nhttps://contaq.io/search\n\nOnce the list is ready, you can export it to CSV format and start reaching out to new prospects ;-)\n\nBest,\nContaq.io Team\n''',
        "Contaq.io Team <no-reply@mg.contaq.io>", [request.user.email])
    redirect = reverse('subscriptions:subscription_details')
    return HttpResponseRedirect(redirect)
