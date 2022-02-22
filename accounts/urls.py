from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from accounts.views import SignInView

# urlpatterns = [
#     path('signin', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('refreshtoken', TokenRefreshView.as_view(), name='token_refresh'),
# ]

urlpatterns = [
    path('signin', SignInView.as_view(), name='signin'),
]
