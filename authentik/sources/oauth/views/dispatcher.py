"""Dispatch OAuth views to respective views"""

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from structlog.stdlib import get_logger

from authentik.sources.oauth.models import OAuthSource
from authentik.sources.oauth.short_urls import resolve_public_source_slug
from authentik.sources.oauth.types.registry import RequestKind, registry

LOGGER = get_logger()


@method_decorator(csrf_exempt, name="dispatch")
class DispatcherView(View):
    """Dispatch OAuth Redirect/Callback views to their proper class based on URL parameters"""

    kind = ""

    def dispatch(self, *args, source_slug: str, **kwargs):
        """Find Source by slug and forward request"""
        source = get_object_or_404(OAuthSource, slug=source_slug)
        view = registry.find(source.provider_type, kind=RequestKind(self.kind))
        LOGGER.debug("dispatching OAuth2 request to", view=view, kind=self.kind)
        return view.as_view()(*args, source_slug=source_slug, **kwargs)


@method_decorator(csrf_exempt, name="dispatch")
class ShortDispatcherView(DispatcherView):
    """Dispatch OAuth requests from branded short URLs."""

    def dispatch(self, *args, public_source: str, **kwargs):
        """Resolve public source aliases before dispatching."""
        source_slug = resolve_public_source_slug(public_source)
        return super().dispatch(*args, source_slug=source_slug, **kwargs)
