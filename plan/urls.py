


from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns=[
    path('plans/', ListAllPlans.as_view(), name='list-all-plans'),
    path('PlanPreview/<pk>/', PlanPreview.as_view(), name="product"),
    path('payment-history/', PaymentHistoryListAPIView.as_view(), name='vendor_payment_history'),
    path('stockupdate/', UpdateStockAPIView.as_view(), name='UpdateStockAPIView'),
    path('create-checkout-session/<pk>/',CreateCheckOutSession.as_view(), name='checkout_session'),
    path('webhook/', stripe_webhook_view, name='stripe-webhook'),
    path('last-vendor/', LastVendorAPIView.as_view(), name='last_purchased_plan'),
    path('create-plan/', create_plan, name='create_plan'),
    path('delete-plan/<int:pk>/', delete_plan, name='delete_plan'),


    ]