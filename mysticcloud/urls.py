"""
URL configuration for mysticcloud project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),

    # THIS IS THE MISSING LINE:
    path('i18n/', include('django.conf.urls.i18n')),

    # Main application URLs
    path('', include('home.urls', namespace='home')),
    path('menu/', include('menu.urls', namespace='menu')),
    path('', include('users.urls', namespace='users')),
    path('reservation/', include('reservation.urls', namespace='reservation')),

    # Django-allauth URLs
    path('accounts/', include('allauth.urls')),

    # Password management
    path("change-password/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("reset-password/", auth_views.PasswordResetView.as_view(), name="reset_password"),
    path("password-reset-done/", auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
]

# Development settings
if settings.DEBUG:
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)