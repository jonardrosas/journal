from django.conf.urls import patterns, include, url
from accounts.views import HomePage, UserLoginView, login, SignUp, Authentincate, Authentincate2, Authentincate3
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^admin/', admin.site.urls),
    url(r'^$', login),
    url(r'^accounts/login/$', HomePage.as_view(), name='login'),
    url(r'^accounts/authenticate/$', UserLoginView.as_view(), name='login_authenticate'),
    url(r'^accounts/register/$', SignUp.as_view(), name='login_register'),
    url(r'^accounts/signup/$', Authentincate.as_view(), name='signup_authenticate'),
    url(r'^accounts/signup2/$', Authentincate2.as_view(), name='signup_authenticate2'),
    url(r'^accounts/signup3/$', Authentincate3.as_view(), name='signup_authenticate3'),
)