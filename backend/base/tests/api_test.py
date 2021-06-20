from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
import json
from rest_framework.test import APIClient
User = get_user_model()


class AccountAPITestCase(APITestCase):

    ''' We could've registered a user, at setup.
        Since this is an api test. It's better to deal with endpoints, instead of the models
        '''

    # #Register User
    def test_user_registration(self):
        url = reverse('register')
        client=APIClient()
        data = {
            'name': 'bean123',
            'email': 'beanstalk12@gmail.com',
            'password': 'boom12345'
        }
        response = self.client.post(url, data, format='json')
        print(response)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_user = User.objects.all()
        print(new_user)
        self.assertTrue(new_user)



    '''Duplicating a username should be a bad request'''
    def test_duplicate_username_fail(self):
        url = reverse('register')
        client=APIClient()
        data = {
            'name': 'bean123',
            'email': 'beanstalk12@gmail.com',
            'password': 'boom12345'
        }
        first_response = self.client.post(url, data, format='json')
        print(first_response)



        client=APIClient()
        url = reverse('register')
        data = {
            'username': 'bean123',
            'email': 'beanstalk12@gmail.com',
            'password': 'boom12345'
            
        }
        response = self.client.post(url, data, format='json')
        print(response)
        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
