from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User
from .serializers import UserSerializer


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', inn='0123456789', balance=100)

    def test_user_creation(self):
        self.assertIsInstance(self.user, User)
        self.assertEqual(self.user.username, 'testuser')

    def test_user_balance_update(self):
        self.user.balance += 50
        self.user.save()
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.balance, 150)


class UserListViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('user-list')
        self.user1 = User.objects.create_user(username='user1', password='testpassword1', inn='0111111111', balance=100)
        self.user2 = User.objects.create_user(username='user2', password='testpassword2', inn='0222222222', balance=200)

    def test_user_list_view(self):
        response = self.client.get(self.url)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
