from __future__ import annotations

from dataclasses import dataclass, asdict, field

from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from djstripe.enums import PlanInterval
from djstripe.models import Product, Plan, Subscription
from typing import List, Generator, Dict

from .exceptions import SubscriptionConfigError
from .serializers import PlanSerializer, ProductSerializer


@dataclass
class ProductMetadata:
    """
    Metadata for a Stripe product.
    """
    stripe_id: str
    name: str
    features: List[str]
    price_displays: Dict[str: str] = field(default_factory=dict)
    description: str = ''
    is_default: bool = False

    @classmethod
    def from_stripe_product(cls, stripe_product: Product, **kwargs) -> ProductMetadata:
        defaults = dict(
            stripe_id=stripe_product.id,
            name=stripe_product.name,
            features=[]
        )
        defaults.update(kwargs)
        return cls(
            **defaults
        )


@dataclass
class ProductWithMetadata(object):
    """
    Connects a Stripe product to its ProductMetadata.
    """
    product: Product
    metadata: ProductMetadata

    @property
    def stripe_id(self) -> str:
        return self.metadata.stripe_id or self.product.id

    @cached_property
    def default_plan(self) -> Plan:
        if not ACTIVE_PLAN_INTERVALS:
            raise SubscriptionConfigError(_('At least one plan interval (year or month) must be set!'))
        return self.monthly_plan if ACTIVE_PLAN_INTERVALS[0] == PlanInterval.month else self.annual_plan

    @cached_property
    def annual_plan(self) -> Plan:
        return self._get_plan(PlanInterval.year)

    @cached_property
    def monthly_plan(self) -> Plan:
        return self._get_plan(PlanInterval.month)

    def _get_plan(self, interval: str) -> Plan:
        if self.product:
            try:
                return self.product.plan_set.get(interval=interval, interval_count=1)
            except (Plan.DoesNotExist, Plan.MultipleObjectsReturned):
                raise SubscriptionConfigError(_(
                    f'Unable to select a "{interval}" plan for {self.product}. '
                    'Have you setup your Stripe objects and run ./manage.py djstripe_sync_plans_from_stripe? '
                    'You can also hide this plan interval by removing it from ACTIVE_PLAN_INTERVALS in '
                    'apps/subscriptions/metadata.py'
                ))

    def get_annual_price_display(self) -> str:
        return self.get_price_display(self._get_plan(PlanInterval.year))

    def get_monthly_price_display(self) -> str:
        return self.get_price_display(self._get_plan(PlanInterval.month))

    def get_price_display(self, plan: Plan) -> str:
        # if the price display info has been explicitly overridden, use that
        if plan.interval in self.metadata.price_displays:
            return self.metadata.price_displays[plan.interval]
        else:
            # otherwise get it from the plan
            from apps.subscriptions.helpers import get_friendly_currency_amount
            return get_friendly_currency_amount(plan)

    def to_dict(self):
        """
        :return: a JSON-serializable dictionary for this object,
        usable in an API.
        """
        def _serialized_plan_or_none(plan):
            return PlanSerializer(plan).data if plan else None

        return {
            'product': ProductSerializer(self.product).data,
            'metadata': asdict(self.metadata),
            'default_plan': _serialized_plan_or_none(self.default_plan),
            'annual_plan': _serialized_plan_or_none(self.annual_plan),
            'monthly_plan': _serialized_plan_or_none(self.monthly_plan),
        }


@dataclass
class PlanIntervalMetadata(object):
    """
    Metadata for a Stripe product.
    """
    interval: str
    name: str


def get_plan_name_for_interval(interval: str) -> str:
    return {
        PlanInterval.year: _('Annual'),
        PlanInterval.month: _('Monthly'),
    }.get(interval, _('Custom'))


def get_active_plan_interval_metadata() -> List[PlanIntervalMetadata]:
    return [
        PlanIntervalMetadata(interval=interval, name=get_plan_name_for_interval(interval))
        for interval in ACTIVE_PLAN_INTERVALS
    ]

# Active plan intervals. Only allowed values are "PlanInterval.month" and "PlanInterval.year"
# Remove one of them to only allow monthly/annual pricing.
# The first element is considered the default
ACTIVE_PLAN_INTERVALS = [
        PlanInterval.month
]


# These are the products that will be shown to users in the UI and allowed to be associated
# with plans on your side
ACTIVE_PRODUCTS = [
    ProductMetadata(stripe_id='prod_LWH7aTMeYzdOBh', name='Standard Plan', features=["500 credits", 'Standard Plan Feature 2', 'Standard Plan Feature 3'], price_displays={}, description='The Standard Plan plan', is_default=False),
    ProductMetadata(stripe_id='prod_LWenKEl8C9oVtX', name='Pro Plan', features=["1000 credits", 'Pro Plan Feature 2', 'Pro Plan Feature 3'], price_displays={}, description='The Pro Plan plan', is_default=True),
    ProductMetadata(stripe_id='prod_LWenXHk8knDwGt', name='Elite Plan', features=["2000 credits", 'Elite Plan Feature 2', 'Elite Plan Feature 3'], price_displays={}, description='The Elite Plan plan', is_default=False),
]

ACTIVE_PRODUCTS_BY_ID = {
    p.stripe_id: p for p in ACTIVE_PRODUCTS
}


def get_active_products_with_metadata() -> Generator[ProductWithMetadata]:
    # if we have set active products in metadata then filter the full list
    if ACTIVE_PRODUCTS:
        for product_meta in ACTIVE_PRODUCTS:
            try:
                yield ProductWithMetadata(
                    product=Product.objects.get(id=product_meta.stripe_id),
                    metadata=product_meta,
                )
            except Product.DoesNotExist:
                raise SubscriptionConfigError(_(
                    f'No Product with ID "{product_meta.stripe_id}" found! '
                    f'This is coming from the "{product_meta.name}" Product in the ACTIVE_PRODUCTS variable '
                    f'in metadata.py. '
                    f'Please make sure that all products in ACTIVE_PRODUCTS have a valid stripe_id and that '
                    f'you have synced your Product database with Stripe.'
                ))
    else:
        # otherwise just use whatever is in the DB
        for product in Product.objects.all():
            yield ProductWithMetadata(
                product=product,
                metadata=ACTIVE_PRODUCTS_BY_ID.get(product.id, ProductMetadata.from_stripe_product(product))
            )
        else:
            raise SubscriptionConfigError(_(
                'It looks like you do not have any Products in your database. '
                'In order to use subscriptions you first have to setup Stripe billing and sync it '
                'with your local data.'
            ))


def get_product_with_metadata(djstripe_product: Product) -> ProductWithMetadata:
    if djstripe_product.id in ACTIVE_PRODUCTS_BY_ID:
        return ProductWithMetadata(
            product=djstripe_product,
            metadata=ACTIVE_PRODUCTS_BY_ID[djstripe_product.id]
        )
    else:
        return ProductWithMetadata(
            product=djstripe_product,
            metadata=ProductMetadata.from_stripe_product(djstripe_product)
        )


def get_product_and_metadata_for_subscription(subscription: Subscription) -> ProductWithMetadata:
    if not subscription:
        return None
    return get_product_with_metadata(subscription.plan.product)
