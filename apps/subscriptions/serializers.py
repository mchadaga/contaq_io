from djstripe.models import Product, Plan, Subscription
from rest_framework import serializers


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('id', 'current_period_start', 'current_period_end', 'cancel_at_period_end',
                  'start_date', 'status', 'quantity')


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name')


class PlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = ('id', 'nickname', 'amount')
