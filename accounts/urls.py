from django.urls import path
from .views import AuthenticateCustomerView, AuthenticateBloggerView, AuthenticateErranderView, AuthenticateAdminView, CustomerRequestPassswordResetVew, ErranderRequestPassswordResetVew, PasswordResetView
from operations.views import CustomerVerifyView

app_name= 'accounts'

urlpatterns = [
    path('auth/customer/', AuthenticateCustomerView.as_view(), name='auth_customer'),
    path('auth/errander/', AuthenticateErranderView.as_view(), name='auth_errander'),
    path('auth/blogger/', AuthenticateBloggerView.as_view(), name='auth_blogger'),
    path('auth/admin/', AuthenticateAdminView.as_view(), name='auth_admin'),
    path('customer/activate/<token>/', CustomerVerifyView.as_view(), name='Verify_Customer'),
    path('customer/reset-password-request/', CustomerRequestPassswordResetVew.as_view(), name='customer_request_password'),
    path('errander/reset-password-request/', ErranderRequestPassswordResetVew.as_view(), name='errander_request_password'),
    path('reset-password/', PasswordResetView.as_view(), name="reset-password")
]