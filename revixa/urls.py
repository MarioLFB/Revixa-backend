from django.contrib import admin
from django.urls import path, include
from api.views import CreateUserView, MyTokenObtainPairView, UpdateEmailView, UpdatePasswordView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/register/', CreateUserView.as_view(), name="register"),
    path('api/token/', MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('api/user/update-email/', UpdateEmailView.as_view(), name="update_email"),
    path('api/user/update-password/', UpdatePasswordView.as_view(), name="update_password"),
    path('api-auth/', include("rest_framework.urls")),
    path('social/', include('social.urls')),
    path('reviews/', include('reviews.urls')),
]
