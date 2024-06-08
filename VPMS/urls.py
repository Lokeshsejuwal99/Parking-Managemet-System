from django.contrib import admin
from django.urls import path, include
from Vehicle.views import LandingView, VehicleSignupview, logout
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("vehicle/", include("Vehicle.urls", namespace="Vehicle")),
    path("owners/", include("Owner.urls", namespace="Owner")),
    path("", LandingView.as_view(), name="landing-page"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout, name="logout"),
    path("signup/", VehicleSignupview.as_view(), name="signup"),
    # path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
