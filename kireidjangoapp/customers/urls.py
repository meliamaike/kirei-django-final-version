from django.urls import path

from customers import views

from django.contrib.auth import views as auth_views
from home.views import index
from django.conf import settings
from django.conf.urls.static import static

app_name = "customers"

urlpatterns = [
    path("register/", views.signup_view, name="register"),
    path("login/", views.customer_login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("password_reset/", views.password_reset, name="password_reset"),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="customers/password/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="customers/password/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="customers/password/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("profile/", views.profile, name="profile"),
    #path("profile/edit", views.edit_profile_image, name="edit_profile_image"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



