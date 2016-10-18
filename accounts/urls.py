from django.conf.urls import url, include
from .views import (
    ResetPasswordView, HomePage, PasswordResetConfirmView
)

urlpatterns = [
    url(r'^password_reset/', ResetPasswordView.as_view(), name='reset_password'),
    url(r'^confirm_reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    url(r'^login/$', HomePage.as_view(), name='login'),
]