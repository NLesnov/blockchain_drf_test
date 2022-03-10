from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from .models import Token
from .serializers import TokenSerializer


class ListTokenResultsPagination(PageNumberPagination):
    page_size = 200
    max_page_size = 500


class CreateTokenView(APIView):
    ...


class ListTokenView(GenericAPIView, ListModelMixin):
    queryset = Token.objects.all()
    pagination_class = ListTokenResultsPagination
    serializer_class = TokenSerializer


class GetTokenTotalSupplyView(APIView):
    ...
