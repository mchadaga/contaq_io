from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from djstripe.enums import PlanInterval
from djstripe.settings import djstripe_settings

from ..decorators import redirect_subscription_errors
from ..helpers import get_subscription_urls, get_payment_metadata_from_request
from ..metadata import get_active_products_with_metadata, \
    get_product_and_metadata_for_subscription, ACTIVE_PLAN_INTERVALS, get_active_plan_interval_metadata
from ..models import SubscriptionModelBase


@redirect_subscription_errors
@login_required
def subscription(request, subscription_holder=None):
    subscription_holder = subscription_holder if subscription_holder else request.user
    if subscription_holder.has_active_subscription():
        return _view_subscription(request, subscription_holder)
    else:
        return _upgrade_subscription(request, subscription_holder)


def _view_subscription(request, subscription_holder: SubscriptionModelBase):
    """
    Show user's active subscription
    """
    assert subscription_holder.has_active_subscription()
    return render(request, 'subscriptions/view_subscription.html', {
        'active_tab': 'subscription',
        'subscription': subscription_holder.active_stripe_subscription,
        'subscription_urls': get_subscription_urls(subscription_holder),
        'friendly_payment_amount': subscription_holder.get_subscription_metadata().get_price_display(
            subscription_holder.active_stripe_subscription.plan
        ),
        'product': get_product_and_metadata_for_subscription(subscription_holder.active_stripe_subscription),
    })


def _upgrade_subscription(request, subscription_holder):
    """
    Show subscription upgrade form / options.
    """
    assert not subscription_holder.has_active_subscription()

    active_products = list(get_active_products_with_metadata())
    default_products = [p for p in active_products if p.metadata.is_default]
    default_product = default_products[0] if default_products else active_products[0]

    def _to_dict(product_with_metadata):
        # for now, just serialize the minimum amount of data needed for the front-end
        product_data = {}
        if PlanInterval.year in ACTIVE_PLAN_INTERVALS:
            product_data['annual_plan'] = {
                'stripe_id': product_with_metadata.annual_plan.id,
                'payment_amount': product_with_metadata.get_annual_price_display(),
                'interval': PlanInterval.year,
            }
        if PlanInterval.month in ACTIVE_PLAN_INTERVALS:
            product_data['monthly_plan'] = {
                'stripe_id': product_with_metadata.monthly_plan.id,
                'payment_amount': product_with_metadata.get_monthly_price_display(),
                'interval': PlanInterval.month,
            }
        return product_data

    if settings.STRIPE_PAYMENT_MODE == 'checkout':
        template_name = 'subscriptions/upgrade_subscription_checkout.html'
    else:
        template_name = 'subscriptions/upgrade_subscription_elements.html'

    return render(request, template_name, {
        'active_tab': 'subscription',
        'stripe_api_key': djstripe_settings.STRIPE_PUBLIC_KEY,
        'default_product': default_product,
        'active_products': active_products,
        'active_products_json': {str(p.stripe_id): _to_dict(p) for p in active_products},
        'active_plan_intervals': get_active_plan_interval_metadata(),
        'default_to_annual': ACTIVE_PLAN_INTERVALS[0] == PlanInterval.year,
        'subscription_urls': get_subscription_urls(subscription_holder),
        'payment_metadata': get_payment_metadata_from_request(request),
    })


@login_required
def subscription_demo(request, subscription_holder=None):
    subscription_holder = subscription_holder if subscription_holder else request.user
    return render(request, 'subscriptions/demo.html', {
        'active_tab': 'subscription_demo',
        'subscription': subscription_holder.active_stripe_subscription,
        'product': get_product_and_metadata_for_subscription(
            subscription_holder.active_stripe_subscription
        ),
        'subscription_urls': get_subscription_urls(subscription_holder)
    })


@login_required
def subscription_gated_page(request, subscription_holder=None):
    subscription_holder = subscription_holder if subscription_holder else request.user
    if not subscription_holder.has_active_subscription():
        return render(request, 'subscriptions/subscription_required.html')
    else:
        return render(request, 'subscriptions/subscription_gated_page.html')
