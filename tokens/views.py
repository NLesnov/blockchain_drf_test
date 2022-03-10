from web3 import Web3

from django.utils.crypto import get_random_string
from django.conf import settings

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from .models import Token
from .serializers import TokenSerializer


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


class CreateTokenView(GenericAPIView, CreateModelMixin):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer

    def perform_create(self, serializer):
        unique_hash = get_random_string(length=20)
        serializer.save(
            unique_hash=unique_hash
        )
        transaction_hash = self.create_smart_contract(
            owner=serializer.data['owner'],
            unique_hash=serializer.data['unique_hash'],
            media_url=serializer.data['media_url'],
        )
        serializer.save(
            tx_hash=transaction_hash
        )

    def create_smart_contract(self, owner, unique_hash, media_url):
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
        transaction_hash = w3.eth.send_raw_transaction(signed_transaction)
        return transaction_hash


class ListTokenView(GenericAPIView, ListModelMixin):
    queryset = Token.objects.all()
    pagination_class = ListTokenResultsPagination
    serializer_class = TokenSerializer


class GetTokenTotalSupplyView(APIView):
    ...
