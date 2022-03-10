from django.utils.crypto import get_random_string
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from .models import Token
from .serializers import TokenSerializer


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
        self.create_smart_contract(serializer.data)
        
    def create_smart_contract(self, token_data):
        ...


class ListTokenView(GenericAPIView, ListModelMixin):
    queryset = Token.objects.all()
    pagination_class = ListTokenResultsPagination
    serializer_class = TokenSerializer


class GetTokenTotalSupplyView(APIView):
    ...
