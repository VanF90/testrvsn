from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import TransferService
from .serializers import TransactionSerializer


class TransferView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        sender_id = request.data.get('sender_id')
        if type(request.data) == dict:
            receiver_inns = request.data.get('receiver_inns')
        else:
            receiver_inns = request.data.getlist('receiver_inns')
        amount = Decimal(request.data.get('amount'))

        if amount <= 0:
            return Response({'detail': 'Transfer amount must be greater than zero'}, status=400)

        if not sender_id or not receiver_inns or not amount:
            return Response({'detail': 'Invalid data'}, status=400)

        try:
            transactions = TransferService.make_transfer(sender_id, receiver_inns, amount)
        except Exception as e:
            return Response({'detail': str(e)}, status=400)

        transactions_data = TransactionSerializer(transactions, many=True).data
        return Response({'detail': 'Transfer completed', 'transactions': transactions_data}, status=200)
