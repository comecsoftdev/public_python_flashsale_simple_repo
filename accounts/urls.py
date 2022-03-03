from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from accounts.views import SignInView, SignOutView, RefreshTokenView

# urlpatterns = [
#     path('signin', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('refreshtoken', TokenRefreshView.as_view(), name='token_refresh'),
# ]

urlpatterns = [
    # sign in
    path('signin', SignInView.as_view(), name='signin'),
    # sign out
    path('signout', SignOutView.as_view(), name='signout'),
    # refresh token
    path('refreshtoken', RefreshTokenView.as_view(), name='refreshtoken'),
]
