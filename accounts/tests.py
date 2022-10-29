from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTestCase(TestCase):
    """Test case for User object interaction"""
    username = "johndoe"
    email = "doe@gmail.com"
    password = "pass11234"
    role = "DEVELOPER"
    usage = "PERSONAL"

    def setUp(self):
        self.user = User(username=self.username,
                         email=self.email, password=self.password, role=self.role, usage=self.usage)
        self.user.save()

    def tearDown(self):
        User.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.user, User))

    def test_save_method(self):
        users = User.objects.all()
        self.assertTrue(len(users) == 1)
