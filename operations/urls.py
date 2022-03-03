from django.urls import path
from .views import (CustomerCreateListView, CustomerDetailView, 
                    ErranderCreateListView, ErranderDetailView, ErranderVerifyView, ErranderDeclineView,
                    )

app_name= 'operations'

urlpatterns = [
    path('customer/', CustomerCreateListView.as_view(), name='Create_List_Customer'),
    path('customer/<int:id>/', CustomerDetailView.as_view(), name='Detail_Customer'),
    path('errander/', ErranderCreateListView.as_view(), name='Create_List_Errander'),
    path('errander/<int:id>/', ErranderDetailView.as_view(), name='Detail_Errander'),
    path('errander/verify/<int:id>/', ErranderVerifyView.as_view(), name='Verify_Errander'),
    path('errander/decline/<int:id>/', ErranderDeclineView.as_view(), name='Decline_Errander'),
]