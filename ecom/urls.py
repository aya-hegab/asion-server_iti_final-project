from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from users.views import *
from order.views import *
from plan.views import *



urlpatterns = [

    path('admin/', admin.site.urls),
    path('API/',include('product.urls')),
    path('API/',include('category.urls')),
    path('API/',include('order.urls')),
    path('API/',include('contactUs.urls')),
    path('API/', include('banner.urls')),
    path('api/', include('users.urls')),
    path('api/', include('plan.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/wishlist/', include('wishlist.urls')),
    path('api/delivaryman/', include('delivaryman.urls')),
    path('API/Review/',include('review.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('verify-email/', verify_email, name='verify_email'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('forget-password/', ForgetPasswordView.as_view(), name='forget_password'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('api/admin/statistics/', get_statistics, name='admin-statistics'),
    path('profile/', UserDelete.as_view(), name='user-delete'),
    path('order-statistics/', order_statistics, name='order_statistics'),
    path('profile/<int:pk>/', UserUpdate.as_view(), name='user-update'),
    path('user-profile/<int:user_id>/', UserProfileView.as_view(), name='user-profile'),
    path('add-user/', AddUserView.as_view(), name='add_user'),
    path('api/admin/plan-statistics/', PlanStatistics.as_view(), name='plan_statistics'),
     path('best-selling-products/', best_selling_products, name='best_selling_products'),
    

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
