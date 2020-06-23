from django.test import TestCase, Client

from django.urls import reverse
from django.contrib.auth.models import User
from NA_WebApp.models import Profile
import json


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.profile_url = reverse('NA_WebApp-profile')

        self.user = User.objects.create_user('test1@no.com', 'özgecangal@no.com', '30071985Fe')
        print("Saved User name : " + self.user.username)

        logged_in = self.client.login(username='test1@no.com', password='30071985Fe')
        print("Is Log-in Succeed ?: " + str(logged_in))

    def test_profile(self):
        response = self.client.get(self.profile_url)
        print("We got from '" + self.profile_url + "'  -> status code : " + str(response.status_code))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'NA_WebApp/auth/profile.html')
