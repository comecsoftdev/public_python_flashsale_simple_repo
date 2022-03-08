from django.urls import path

from flashsale.view import basic_data
from flashsale.view import store

app_name = 'flashsale'
urlpatterns = [
    # get initial user data, category and address
    path('getinituserdata', basic_data.GetInitUserDataView.as_view(), name='getinituserdata'),
    # register store
    path('registerstore', store.RegisterStoreView.as_view(), name='registerstore'),
    # unregister store
    path('unregisterstore', store.UnRegisterStoreView.as_view(), name='unregisterstore'),
]
