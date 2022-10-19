from core import reports, views
from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.SimpleRouter()

router.register(r"categories", views.CategoryModelViewSet, basename="category")
router.register(r"transactions", views.TransactionModelViewSet, basename="transaction")

urlpatterns = [
    path("login/", obtain_auth_token, name="obtain-auth-token"),
    path("currencies/", views.CurrencyListAPIView.as_view(), name="currencies"),
    path("report/", views.TRanactionReportAPIView.as_view(), name="report"),
] + router.urls