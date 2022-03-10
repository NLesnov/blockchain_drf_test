from rest_framework import status
from web3 import Web3

from django.utils.crypto import get_random_string
from django.conf import settings

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import Token
from .serializers import TokenSerializer, TotalSupplySerializer


w3 = Web3(Web3.HTTPProvider(settings.BLOCKCHAIN_PROVIDER))

if settings.USE_GETH_POA:
    from web3.middleware import geth_poa_middleware
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract_abi = settings.CONTRACT_ABI
contract_address = settings.CONTRACT_ADDRESS

contract = w3.eth.contract(
    address=contract_address,
    abi=contract_abi,
)


class ListTokenResultsPagination(PageNumberPagination):
    page_size = 200
    max_page_size = 500


class CreateTokenView(CreateAPIView):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_instance = self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        token_with_hash = self.inject_transaction_hash(token_instance)
        serializer = self.get_serializer(token_with_hash)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def inject_transaction_hash(self, token):
        """
        Метод вызывает создание токена в блокчейне,
        записывает хэш транзакции создания в инстанс Токена
        """
        transaction_hash = self.create_smart_contract(
                owner=token.owner,
                unique_hash=token.unique_hash,
                media_url=token.media_url,
        )
        token.tx_hash = transaction_hash
        token.save()
        return token

    def perform_create(self, serializer):
        # todo: hash совершенно не unique, но соответствует ТЗ
        unique_hash = get_random_string(length=20)
        token = serializer.save(
            unique_hash=unique_hash
        )
        return token

    def create_smart_contract(self, owner, unique_hash, media_url):
        """
        todo: Сделать асинхронным
        Метод создания токена в блокчейне, возвращает хэш транзакции создания
        """
        nonce = w3.eth.get_transaction_count(
            settings.PUBLIC_VALLET_ADDRESS
        )
        transaction = contract.functions.mint(
            owner=owner,
            uniqueHash=unique_hash,
            mediaURL=media_url,
        ).buildTransaction(
            {
                'nonce': nonce
            }
        )
        signed_transaction = w3.eth.account.sign_transaction(
            transaction,
            private_key=settings.PRIVATE_KEY
        )
        transaction_hash = w3.eth.send_raw_transaction(
            signed_transaction.rawTransaction
        )
        return transaction_hash


class ListTokenView(ListAPIView):
    queryset = Token.objects.all()
    pagination_class = ListTokenResultsPagination
    serializer_class = TokenSerializer


class GetTokenTotalSupplyView(APIView):
    serializer_class = TotalSupplySerializer

    def get(self, request):
        total_supply = contract.functions.totalSupply().call()
        serializer = self.serializer_class(data={'total_supply': total_supply})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
