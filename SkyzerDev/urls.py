"""
URL configuration for SkyzerDev project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from SkyzerDev import views, settings
from .sitemaps import StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path('blog/', include('lotus.urls', namespace='lotus')),
    path('', views.index, name='index'),
    path('nitrado_server_guardian/', views.server_guardian, name='nitrado_server_guardian'),
    path('robots.txt', views.robots, name='robots'),
    path('about/', views.about, name='about'),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps},
         name="django.contrib.sitemaps.views.sitemap"),
    path("auth/", include('mozilla_django_oidc.urls')),
    path("account/", views.account, name="account"),
    path("account/stripe/email/", views.update_stripe_email, name="update_stripe_email"),
    path("nitrado/login/", views.nitrado_login, name="nitrado_login"),
    path("nitrado/callback/", views.nitrado_callback, name="nitrado_callback"),
    path("premium/", views.premium_features, name="premium_features"),
    path("logout/", views.logout, name="logout"),
    path("commands/", views.commands, name="commands"),
    path("premium_commands/", views.premium_commands, name="premium_commands"),
    path("terms_of_service", views.terms_of_service, name="terms_of_service"),
    path("privacy_policy", views.privacy_policy, name="privacy_policy"),
    path("cookies", views.cookies, name="cookies"),
    path("ctf/", include('scoreboard.urls', namespace="scoreboard"), name="scoreboard"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
