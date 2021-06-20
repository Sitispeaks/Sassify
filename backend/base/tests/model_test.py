from django.test import TestCase
from django.contrib.auth.models import User
# from .models import Product
# Create your tests here.
# User=get_user_model()

# print(User.objects.all())
class AccountTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="ashok das",
            password="boom12345"
        )

        self.other_user = User.objects.create_user(
            username="bean",
            password="boom12345"
        )

    def test_profile_created(self):
        user = User.objects.all()

            #since we created 2 users, we should have 2 profiles
        self.assertEqual(user.count(), 2)

    def test_delete_user_deletes_profile(self):
        self.user.delete()

        profiles = User.objects.all()
        self.assertEqual(profiles.count(), 1)



    def test_profile_username(self):
        profile = User.objects.values()
        self.assertEqual(profile[0]['username'], self.user.username)