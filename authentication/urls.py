from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, CustomTokenObtainPairView

urlpatterns = [
    # Registration endpoint
    path('register/', RegisterView.as_view(), name='register'),
    
    # Login endpoint (obtains access and refresh tokens)
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Token refresh endpoint (to get a new access token when the old one expires)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]