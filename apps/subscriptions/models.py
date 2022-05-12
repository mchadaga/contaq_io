from django.db import models
from django.db.models import F, Q
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from djstripe.enums import SubscriptionStatus

from apps.subscriptions.metadata import get_product_and_metadata_for_subscription


class SubscriptionModelBase(models.Model):
    """
    Helper class to be used with Stripe Subscriptions.

    Assumes that the associated subclass is a django model containing a
    subscription field that is a ForeignKey to a djstripe.Subscription object.
    """
    # subclass should override with appropriate foreign keys as needed
    subscription = models.ForeignKey('djstripe.Subscription', null=True, blank=True, on_delete=models.SET_NULL,
                                     help_text=_("The associated Stripe Subscription object, if it exists"))
    billing_details_last_changed = models.DateTimeField(
        default=timezone.now,
        help_text=_(
            'Updated every time an event that might trigger billing happens.'
        )
    )
    last_synced_with_stripe = models.DateTimeField(null=True, blank=True,
                                                   help_text=_('Used for determining when to next sync with Stripe.'))

    class Meta:
        abstract = True

    @cached_property
    def active_stripe_subscription(self):
        if self.subscription and self.subscription.status == SubscriptionStatus.active:
            return self.subscription
        return None

    def has_active_subscription(self):
        return self.active_stripe_subscription is not None

    @classmethod
    def get_items_needing_sync(cls):
        return cls.objects.filter(
            Q(last_synced_with_stripe__isnull=True) | Q(last_synced_with_stripe__lt=F('billing_details_last_changed')),
            subscription__status=SubscriptionStatus.active,
        )

    def get_quantity(self):
        # if you use "per-seat" billing, override this accordingly
        return 1

    def get_subscription_metadata(self):
        if self.active_stripe_subscription is None:
            return None
        return get_product_and_metadata_for_subscription(self.active_stripe_subscription)
