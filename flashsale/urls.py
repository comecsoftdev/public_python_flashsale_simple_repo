from django.urls import path

from flashsale.view import basic_data

app_name = 'flashsale'
urlpatterns = [
    # get initial user data, category and address
    path('getinituserdata', basic_data.GetInitUserDataView.as_view(), name='getinituserdata'),
]
