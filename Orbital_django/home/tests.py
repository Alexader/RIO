from django.test import TestCase
from models import User


class TestUser(TestCase):
    def test_create_user(self):
        new_user = User()
        new_user.save()
        count = User.objects.all().count()
        self.assertEqual(count, 1)

    def test_user_default_property(self):
        new_user = User()
        new_user.save()
        portrait_url = new_user.portrait_url
        is_active = new_user.is_active
        nickname = new_user.nickname
        self.assertEqual(portrait_url, "media/portrait/default_portrait.png")
        self.assertEqual(is_active, True)
        self.assertEqual(nickname, "")

