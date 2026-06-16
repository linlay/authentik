"""authentik OAuth source root urls"""

from django.urls import path

from authentik.sources.oauth.types.registry import RequestKind
from authentik.sources.oauth.views.dispatcher import ShortDispatcherView

urlpatterns = [
    path(
        "oauth/<slug:public_source>/login/",
        ShortDispatcherView.as_view(kind=RequestKind.REDIRECT),
        name="oauth-client-login",
    ),
    path(
        "oauth/<slug:public_source>/callback/",
        ShortDispatcherView.as_view(kind=RequestKind.CALLBACK),
        name="oauth-client-callback",
    ),
]
