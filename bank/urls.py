from core import reports, views
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.SimpleRouter()

router.register(r"categories", views.CategoryModelViewSet, basename="category")
router.register(r"transactions", views.TransactionModelViewSet, basename="transaction")
router.register(r"currencies", views.CurrencyModelViewSet, basename="currency")

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path('__debug__/', include('debug_toolbar.urls')),
    path("login/", obtain_auth_token, name="obtain-auth-token"),
    path("report/", views.TransactionReportAPIView.as_view(), name="report"),
] + router.urls