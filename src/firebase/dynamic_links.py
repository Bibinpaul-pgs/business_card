# builtins
import json

# django
from django.conf import settings

# third party
import requests


class DynamicLinks:
    FIREBASE_API_URL = 'https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key={}'

    def __init__(self, domain, bundleId='', timeout=10):
        self.api_key = json.loads(settings.FIREBASE_CONFIG['FIREBASE_WEBAPP_CONFIG'])['apiKey']
        self.domain = domain
        self.bundleId = bundleId
        self.timeout = timeout
        self.api_url = self.FIREBASE_API_URL.format(self.api_key)

    def generate_dynamic_link(self, link, short=True, params={}):
        payload = {
            "dynamicLinkInfo": {
                "domainUriPrefix": self.domain,
                "link": link,
                "androidInfo": {
                    "androidPackageName": self.bundleId,
                },
            },
            "suffix": {
                "option": "SHORT" if short else "UNGUESSABLE"
            }
        }
        payload['dynamicLinkInfo'].update(params)

        response = requests.post(self.api_url, json=payload, timeout=self.timeout)

        data = response.json()

        if not response.ok:
            raise FirebaseDynamicLinksError(data)

        return data['shortLink']


class FirebaseDynamicLinksError(Exception):
    pass
