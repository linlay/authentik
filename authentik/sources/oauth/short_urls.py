"""Helpers for branded OAuth source URLs."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from authentik.sources.oauth.models import OAuthSource

PUBLIC_SOURCE_SLUGS = {
    "google": "zenmind-google",
}


def source_public_slug(source: "OAuthSource") -> str:
    """Return the public URL slug for a source."""
    for public_slug, source_slug in PUBLIC_SOURCE_SLUGS.items():
        if source.slug == source_slug:
            return public_slug
    return source.slug


def resolve_public_source_slug(public_source: str) -> str:
    """Resolve a public URL slug to the internal source slug."""
    return PUBLIC_SOURCE_SLUGS.get(public_source, public_source)
