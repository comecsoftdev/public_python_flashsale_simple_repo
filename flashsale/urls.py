from django.urls import path

from flashsale.view import basic_data, store, product, review

app_name = 'flashsale'
urlpatterns = [
    # get initial user data, category and address
    path('getinituserdata', basic_data.GetInitUserDataView.as_view(), name='getinituserdata'),
    # register store
    path('registerstore', store.RegisterStoreView.as_view(), name='registerstore'),
    # unregister store
    path('unregisterstore', store.UnRegisterStoreView.as_view(), name='unregisterstore'),
    # register product
    path('registerproduct', product.RegisterProductView.as_view(), name='registerproduct'),
    # unregister product
    path('unregisterproduct', product.UnRegisterProductView.as_view(), name='unregisterproduct'),
    # register review
    path('registerreview', review.RegisterReviewView.as_view(), name='registerreview'),
    # unregister review
    path('unregisterreview', review.UnRegisterReviewView.as_view(), name='unregisterreview'),
    # get reviews with store_id
    path('getreviews', review.GetReviewsView.as_view(), name='getreviews'),
]
