from django.urls import path

from purchase.views import PurchaseCreate


app_name = 'purchase'

urlpatterns = [
    path('create/<int:package_id>/', PurchaseCreate.as_view(), name="create_purchase")
]
