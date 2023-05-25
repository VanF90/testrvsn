from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from .models import Transaction


class TransactionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.sender = User.objects.create_user(username='sender', inn='0123456789', balance=500)
        self.receivers = [
            User.objects.create_user(username=f'receiver{i}', inn=f'098765432{i}', balance=0)
            for i in range(1, 4)
        ]

    def test_successful_transfer(self):
        response = self.client.post(reverse('transfer'), data={
            'sender_id': self.sender.id,
            'receiver_inns': [user.inn for user in self.receivers],
            'amount': 300,
        })

        self.assertEqual(response.status_code, 200)
        self.sender.refresh_from_db()
        for user in self.receivers:
            user.refresh_from_db()
        self.assertEqual(self.sender.balance, 200)
        for user in self.receivers:
            self.assertEqual(user.balance, 100)
        self.assertEqual(Transaction.objects.count(), 3)

    def test_insufficient_funds(self):
        response = self.client.post(reverse('transfer'), data={
            'sender_id': self.sender.id,
            'receiver_inns': [user.inn for user in self.receivers],
            'amount': 600,
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], 'Insufficient funds')

    def test_receiver_not_found(self):
        response = self.client.post(reverse('transfer'), data={
            'sender_id': self.sender.id,
            'receiver_inns': ['non_existent_inn'],
            'amount': 300,
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], 'No receivers found with provided INNs')

    def test_zero_transfer_amount(self):
        response = self.client.post(reverse('transfer'), data={
            'sender_id': self.sender.id,
            'receiver_inns': [user.inn for user in self.receivers],
            'amount': 0,
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], 'Transfer amount must be greater than zero')