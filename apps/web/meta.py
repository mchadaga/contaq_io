from django.conf import settings
from django.contrib.sites.models import Site


def absolute_url(relative_url: str, is_secure: bool = settings.USE_HTTPS_IN_ABSOLUTE_URLS):
    return 'http{}://{}{}'.format(
        's' if is_secure else '',
        Site.objects.get_current().domain,
        relative_url,
    )
