from django.db import transaction
from users.models import User
from .models import Transaction


class TransferService:
    @staticmethod
    def make_transfer(sender_id, receiver_inns, amount):
        sender = User.objects.get(id=sender_id)
        receivers = User.objects.filter(inn__in=receiver_inns)
        receivers_count = receivers.count()

        if not receivers_count:
            raise ValueError("No receivers found with provided INNs")

        amount_per_receiver = amount / receivers_count

        if sender.balance < amount:
            raise ValueError("Insufficient funds")

        transactions_list = []

        with transaction.atomic():
            sender.balance -= amount
            sender.save()

            for receiver in receivers:
                receiver.balance += amount_per_receiver
                receiver.save()
                trans = Transaction.objects.create(sender=sender, receiver=receiver, amount=amount_per_receiver)
                transactions_list.append(trans)

        return transactions_list
