"""
Backend for OpenID Connect Fox UiO
"""

from social_core.backends.open_id_connect import OpenIdConnectAuth


class LifeportalFoxOpenIdConnect(OpenIdConnectAuth):
    name = 'lifeportalfox'
    OIDC_ENDPOINT = 'https://test.api.tsd.usit.no/tsd-oidc-provider/.well-known/openid-configuration'
    EXTRA_DATA = [
        ('expires_in', 'expires_in', True),
        ('refresh_token', 'refresh_token', True),
        ('id_token', 'id_token', True),
        ('other_tokens', 'other_tokens', True),
    ]

    DEFAULT_SCOPE = ['openid', 'email']
    JWT_DECODE_OPTIONS = {'verify_at_hash': False}

    def get_user_details(self, response):
        username_key = self.setting('USERNAME_KEY', default=self.USERNAME_KEY)
        return {'username': response.get(username_key), 'email': response.get('email')}
