import urllib, random, string
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase


class ApiOauth2Test(ResourceTestCase):
    def setUp(self):
        super(ApiOauth2Test, self).setUp()

        # Create a user.
        self.username = ''.join(random.sample(string.letters, 5))
        self.password = ''.join(random.sample(string.letters + string.digits, 7))
        self.user = User.objects.create_user(self.username,
                                             '%s@calories.tester.com' % self.username,
                                             self.password)
        self.client = self.user.oauth2_client.all()[0]

    def tearDown(self):
        super(ApiOauth2Test, self).tearDown()
        self.user.delete()

    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)

    def test_refresh_token_grant_type_password(self):
        data = {
            'grant_type': 'password',
            'username': self.username,
            'password': self.password,
            'client_id': self.client.client_id,
            'client_secret': self.client.client_secret,
            'scope': 'read'
        }
        data = 'grant_type={0}&username={1}&password={2}&' \
               'client_id={3}&client_secret={4}&scope={5}'.format('password',
                                                                  self.username,
                                                                  self.password,
                                                                  self.client.client_id,
                                                                  self.client.client_secret,
                                                                  'read')
        pepe = self.api_client.post('/oauth2/access_token/',
                                    data=data,
                                    CONTENT_TYPE='application/x-www-form-urlencoded')
        import ipdb; ipdb.set_trace()