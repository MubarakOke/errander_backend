from django.urls import path
from .views import (MonitorOperationView, HistoryView,
                    CustomerCreateView, CustomerListView, CustomerDetailView, 
                    ErranderCreateView, ErranderRequestedListView, ErranderVerifiedListView, ErranderDeclinedListView, ErranderDetailView, ErranderVerifyView, ErranderDeclineView,
                    OrderCreateView, OrderUpdateView, OrderInitiatedandRunningListView, OrderCompletedListView, OrderRunningListView,
                    )

app_name= 'operations'

urlpatterns = [
    # Admin URL
    path('admin/monitor/', MonitorOperationView.as_view(), name='Monitor_Admin'),
    path('admin/history/', HistoryView.as_view(), name='History_Admin'),
    # Customer URL
    path('customer/', CustomerCreateView.as_view(), name='Create_Customer'),
    path('customer/list/', CustomerListView.as_view(), name='List_Customer'),
    path('customer/<int:id>/', CustomerDetailView.as_view(), name='Detail_Customer'),
    # Errander URL
    path('errander/', ErranderCreateView.as_view(), name='Create_Errander'),
    path('errander/requested/list/', ErranderRequestedListView.as_view(), name='List_Requested_Errander'),
    path('errander/verified/list/', ErranderVerifiedListView.as_view(), name='List_Verified_Errander'),
    path('errander/declined/list/', ErranderDeclinedListView.as_view(), name='List_Declined_Errander'),
    path('errander/<int:id>/', ErranderDetailView.as_view(), name='Detail_Errander'),
    path('errander/verify/<int:id>/', ErranderVerifyView.as_view(), name='Verify_Errander'),
    path('errander/decline/<int:id>/', ErranderDeclineView.as_view(), name='Decline_Errander'),
    # Order URL
    path('order/', OrderCreateView.as_view(), name='Create_Order'),
    path('order/<int:id>/', OrderUpdateView.as_view(), name='Detail_Order'),
    path('order/uncompleted/list/', OrderInitiatedandRunningListView.as_view(), name='List_Uncompleted_Order'),
    path('order/completed/list/', OrderCompletedListView.as_view(), name='List_Completed_Order'),
    path('order/running/list/', OrderRunningListView.as_view(), name='List_Running_Order'),
    
]