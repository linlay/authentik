from django.urls import reverse
from rest_framework.test import APITestCase

from authentik.core.tests.utils import create_test_admin_user
from authentik.lib.generators import generate_id
from authentik.sources.oauth.models import OAuthSource


class TestOAuthSourceAPI(APITestCase):
    def setUp(self):
        self.source = OAuthSource.objects.create(
            name=generate_id(),
            slug=generate_id(),
            provider_type="openidconnect",
            authorization_url="",
            profile_url="",
            consumer_key=generate_id(),
        )
        self.user = create_test_admin_user()

    def test_patch_no_type(self):
        self.client.force_login(self.user)
        res = self.client.patch(
            reverse("authentik_api:oauthsource-detail", kwargs={"slug": self.source.slug}),
            {
                "authorization_url": f"https://{generate_id()}",
                "profile_url": f"https://{generate_id()}",
                "access_token_url": f"https://{generate_id()}",
            },
        )
        self.assertEqual(res.status_code, 200)

    def test_callback_url_uses_short_path(self):
        """Test callback URL uses branded short path"""
        self.client.force_login(self.user)
        res = self.client.get(
            reverse("authentik_api:oauthsource-detail", kwargs={"slug": self.source.slug}),
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            res.json()["callback_url"],
            f"http://testserver/oauth/{self.source.slug}/callback/",
        )

    def test_callback_url_uses_public_alias(self):
        """Test callback URL uses public alias for ZenMind Google"""
        self.source.slug = "zenmind-google"
        self.source.provider_type = "google"
        self.source.save()
        self.client.force_login(self.user)
        res = self.client.get(
            reverse("authentik_api:oauthsource-detail", kwargs={"slug": self.source.slug}),
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["callback_url"], "http://testserver/oauth/google/callback/")
