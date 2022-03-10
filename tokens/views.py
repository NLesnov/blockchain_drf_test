from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.views import APIView

from .models import Token


class CreateTokenView(APIView):
    ...


class ListTokenView(GenericAPIView, ListModelMixin):
    queryset = Token.objects.all()
    serializer_class = ...


class GetTokenTotalSupplyView(APIView):
    ...
