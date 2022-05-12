from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.permissions import IsAuthenticatedOrHasUserAPIKey
from ..exceptions import SubscriptionConfigError
from ..helpers import create_stripe_checkout_session, create_stripe_portal_session
from ..metadata import get_active_products_with_metadata


class ProductWithMetadataAPI(APIView):
    permission_classes = (IsAuthenticatedOrHasUserAPIKey,)

    def get(self, request, *args, **kw):
        products_with_metadata = get_active_products_with_metadata()
        return Response(
            data=[p.to_dict() for p in products_with_metadata]
        )


class CreateCheckoutSession(APIView):

    def post(self, request):
        subscription_holder = request.user
        price_id = request.POST['priceId']
        checkout_session = create_stripe_checkout_session(
            subscription_holder, price_id, request.user.email
        )
        return Response(checkout_session.url)


class CreatePortalSession(APIView):

    def post(self, request):
        subscription_holder = request.user
        try:
            portal_session = create_stripe_portal_session(subscription_holder)
            return Response(portal_session.url)
        except SubscriptionConfigError as e:
            return Response(str(e), status=500)
