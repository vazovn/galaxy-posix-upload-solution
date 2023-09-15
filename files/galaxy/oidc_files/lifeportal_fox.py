"""
Backend for OpenID Connect Fox UiO
"""

from social_core.backends.open_id_connect import OpenIdConnectAuth


from urllib.parse import urlencode, unquote

from requests_oauthlib import OAuth1
from oauthlib.oauth1 import SIGNATURE_TYPE_AUTH_HEADER

from social_core.utils import url_add_parameters, parse_qs, handle_http_errors, constant_time_compare, SSLHttpAdapter, module_member, parse_qs, user_agent, cache
from social_core.exceptions import AuthFailed, AuthCanceled, AuthUnknownError, AuthMissingParameter, AuthStateMissing, AuthStateForbidden, AuthTokenError
from .base import BaseAuth


import json
import datetime
from calendar import timegm

from jose import jwk, jwt
from jose.jwt import JWTError, JWTClaimsError, ExpiredSignatureError
from jose.utils import base64url_decode

from requests import request, ConnectionError


class LifeportalFoxOpenIdConnect(OpenIdConnectAuth):
    name = 'lifeportalfox'
    OIDC_ENDPOINT = 'https://oidc.fp.educloud.no/ec-oidc-provider'
    EXTRA_DATA = [
        ('expires_in', 'expires_in', True),
        ('refresh_token', 'refresh_token', True),
        ('id_token', 'id_token', True),
        ('other_tokens', 'other_tokens', True),
    ]

    #DEFAULT_SCOPE = ['openid', 'email', 'groups']
    # scope for system user
    #DEFAULT_SCOPE = ['openid', 'email']
    # scope for real user
    DEFAULT_SCOPE = ['openid', 'profile', 'email']
    JWT_DECODE_OPTIONS = {'verify_at_hash': False}

    # This methos is called by ../venv/lib/python3.6/site-packages/social_core/pipeline/social_auth.py
    # The username format is managed by ../venv/lib/python3.6/site-packages/social_core/pipeline/user.py
    def get_user_details(self, response):
        user = response.get('user')
        email = response.get('user')+"@educloud.no"
        return {'username': user, 'email': email}

    # parent method in ../venv/.../social_core/backends/openIid_connect.py
    def find_valid_key(self, id_token):
        from jose.constants import ALGORITHMS
        for key in self.get_jwks_keys():
            if not key.get('alg') :
                 key['alg'] = ALGORITHMS.RS256 
            for key in self.get_jwks_keys():
                print("===== KEY JWKS ===== find_valid_key() === lifeportal_fox.py ====", key)
            rsakey = jwk.construct(key)
            message, encoded_sig = id_token.rsplit('.', 1)
            decoded_sig = base64url_decode(encoded_sig.encode('utf-8'))
            if rsakey.verify(message.encode('utf-8'), decoded_sig):
                return key

    # parent method in in ../venv/.../social_core/backends/oauth.py
    def auth_headers(self):
          import base64
          client_id, client_secret = self.get_key_and_secret()
          auth_key = 'Authorization'
          auth_value = client_id + ':' + client_secret 
          auth_value_bytes = auth_value.encode('ascii')
          auth_value_encoded = base64.b64encode(auth_value_bytes)
          content_key = 'Content-Type'
          content_value = 'application/x-www-form-urlencoded'
          headers = {auth_key:auth_value_encoded,content_key:content_value}
          print("===== METHOD auth_headers() === lifeportal_fox.py ====")
          return headers

    # parent method in ../venv/.../social_core/backends/oauth.py
    @handle_http_errors
    def auth_complete(self, *args, **kwargs):
        """Completes login process, must return user instance"""
        self.process_error(self.data)
        state = self.validate_state()
        data, params = None, None

        print("========= METHOD === auth_complete ()  in lifeportal_fox.py ======")

        if self.ACCESS_TOKEN_METHOD == 'GET':
               params = self.auth_complete_params(state)
        else:
               data = self.auth_complete_params(state)
               url_arguments = {}
               for key,value in  data.items():
                    if key == 'grant_type' or key == 'code' or key == 'redirect_uri':
                        url_arguments[key] = value
               url_arguments['nonce'] = self.get_and_store_nonce(self.authorization_url(), state)
               encoded_url_arguments = urlencode(url_arguments)


        if self.ACCESS_TOKEN_METHOD == 'POST':
               response = self.request_access_token(
                   self.access_token_url()+"?"+encoded_url_arguments,
                   headers=self.auth_headers(),
                   auth=self.auth_complete_credentials(),
                   method=self.ACCESS_TOKEN_METHOD
               )
        elif self.ACCESS_TOKEN_METHOD == 'GET':
               response = self.request_access_token(
                   self.access_token_url(),
                   params=params,
                   headers=self.auth_headers(),
                   auth=self.auth_complete_credentials(),
                   method=self.ACCESS_TOKEN_METHOD
               )

        self.process_error(response)
        return self.do_auth(response['access_token'], response=response,
                            *args, **kwargs)

    # parent method in base.py
    def request(self, url, method='GET', *args, **kwargs):
        kwargs.setdefault('headers', {})
        if self.setting('PROXIES') is not None:
            kwargs.setdefault('proxies', self.setting('PROXIES'))

        if self.setting('VERIFY_SSL') is not None:
            kwargs.setdefault('verify', self.setting('VERIFY_SSL'))
        kwargs.setdefault('timeout', self.setting('REQUESTS_TIMEOUT') or
                          self.setting('URLOPEN_TIMEOUT'))
        if self.SEND_USER_AGENT and 'User-Agent' not in kwargs['headers']:
            kwargs['headers']['User-Agent'] = self.setting('USER_AGENT') or \
                                              user_agent()

        ## Addition Nikolay
        if "token" in url:
             method = 'POST'
             print("=== METHOD ===  request() in lifeportal_fox.py ====", method)
        ## Addition Nikolay
        
        try:
            if self.SSL_PROTOCOL:
                session = SSLHttpAdapter.ssl_adapter_session(self.SSL_PROTOCOL)
                response = session.request(method, url, *args, **kwargs)
            else:
                response = request(method, url, *args, **kwargs)
        except ConnectionError as err:
            raise AuthFailed(self, str(err))
        response.raise_for_status()
        return response
