from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import (
    UserRegister,
    UserDetailView,
    DeveloperRegister,
    DeveloperListView,
    DeveloperProfileDetailView,
    DeveloperProfileListView,
    ClientDeveloperProfileView,
    LogoutView,
    VerifyEmailView
)

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # clients
    path("register/client/", UserRegister.as_view(), name="user-create"),
    path("profile/<str:id>/", UserDetailView.as_view(), name="user-detail"),
    path(
        "developers/<str:developer>/",
        ClientDeveloperProfileView.as_view(),
        name="developer-profile",
    ),
    path("verify-email/<str:uidb64>/<str:token>/", VerifyEmailView.as_view(), name="verify-email"),
    # developers
    path("register/developer/", DeveloperRegister.as_view(), name="developer-create"),
    path(
        "<str:developer>/",
        DeveloperProfileDetailView.as_view(),
        name="developer-detail",
    ),
    path("developers/", DeveloperListView.as_view(), name="developers"),
    path(
        "developers/profile/",
        DeveloperProfileListView.as_view(),
        name="developer-profile",
    ),
]
