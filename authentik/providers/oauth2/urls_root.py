"""authentik oauth_provider urls"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import include, path

from authentik.providers.oauth2.views.authorize import AuthorizationFlowInitView
from authentik.providers.oauth2.views.device_init import DeviceEntryView
from authentik.providers.oauth2.views.github import GitHubUserTeamsView, GitHubUserView
from authentik.providers.oauth2.views.provider import ProviderInfoView
from authentik.providers.oauth2.views.token import TokenView

github_urlpatterns = [
    path(
        "login/oauth/authorize",
        AuthorizationFlowInitView.as_view(github_compat=True),
        name="github-authorize",
    ),
    path(
        "login/oauth/access_token",
        TokenView.as_view(),
        name="github-access-token",
    ),
    path(
        "user",
        GitHubUserView.as_view(),
        name="github-user",
    ),
    path(
        "user/teams",
        GitHubUserTeamsView.as_view(),
        name="github-user-teams",
    ),
]


class BrandedAuthorizationFlowInitView(AuthorizationFlowInitView):
    """Short authorize URL with a friendly empty-query fallback."""

    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET" and not request.GET:
            return redirect("authentik_core:login")
        return super().dispatch(request, *args, **kwargs)


urlpatterns = [
    path("", include(github_urlpatterns)),
    path(
        "o/authorize/",
        BrandedAuthorizationFlowInitView.as_view(),
        name="authorize",
    ),
    path(
        "device",
        login_required(
            DeviceEntryView.as_view(),
        ),
        name="device-login",
    ),
    path(
        ".well-known/oauth-authorization-server/application/o/<slug:application_slug>/",
        ProviderInfoView.as_view(),
        name="providers-oauth2-authorization-server-metadata",
    ),
]
