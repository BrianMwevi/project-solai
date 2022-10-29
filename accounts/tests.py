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

    def test_user_details(self):
        user = User.objects.get(username=self.username)
        self.assertTrue(user.username == self.username)
        self.assertTrue(user.email == self.email)
        self.assertTrue(user.password == self.password)
        self.assertTrue(user.role == self.role)
        self.assertTrue(user.role == self.role)
        self.assertTrue(user.usage == self.usage)
        self.assertTrue(user.is_confirmed == False)

    def test_cannot_change_user_role(self):
        user = User.objects.get(username=self.username)
        user.role = "TRADER"
        user.save()

        # Refresh the database
        updated_user = User.objects.get(username=self.username)
        self.assertTrue(updated_user.role == "DEVELOPER")
