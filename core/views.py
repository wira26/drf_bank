from datetime import datetime
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Category, Currency, Transaction
from core.serializers import CategorySerializer, CurrencySerializer, ReadTransactionSerializer, WriteTransactionSerializer

class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    pagination_class = None

class CategoryModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer

    def  get_queryset(self):
        return Category.objects.filter(user=self.request.user)

class TransactionModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ("description",)
    ordering_fields = ("amount", "date")
    filterset_fields = ("currency__code",)

    def get_queryset(self):
        return Transaction.objects.select_related("currency", "category", "user").filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadTransactionSerializer
        return WriteTransactionSerializer

from rest_framework import serializers
from datetime import date

class PersonSerializer(serializers.Serializer):
    first_name = serializers.CharField(allow_blank=True)
    last_name = serializers.CharField(allow_blank=True)
    birthdate = serializers.DateField()
    age = serializers.SerializerMethodField()

    def get_age(self, obj):
        delta = date.today() - obj.birthdate
        return int(delta.days / 365)

    def validate_birthdate(self, value):
        if value > date.today():
            raise serializers.ValidationError("the birthdate must be a date before today")
        return value

    def validate(self, data):
        if not data["first_name"] and not data["last_name"]:
            raise serializers.ValidationError("isi form")
        return data

class Person:
    def __init__(self, first_name, birthdate):
        self.first_name = first_name
        self.birthdate = birthdate