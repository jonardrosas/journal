from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout
from accounts.views import HomePage, UserLoginView, SignUp, Authentincate, Authentincate2, Authentincate3
from journal_app.views import JournalHomveView
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', admin.site.urls),
    url(r'^journal_app/', include('journal_app.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^$', JournalHomveView.as_view(), name="home"),
    #  url(r'^accounts/login/$', HomePage.as_view(), name='login'),
    url(r'^accounts/authenticate/$', UserLoginView.as_view(), name='login_authenticate'),
    url(r'^accounts/register/$', SignUp.as_view(), name='login_register'),
    url(r'^accounts/signup/$', Authentincate.as_view(), name='signup_authenticate'),
    url(r'^accounts/signup2/$', Authentincate2.as_view(), name='signup_authenticate2'),
    url(r'^accounts/signup3/$', Authentincate3.as_view(), name='password_validate'),
    url(r'^accounts/logout/$', logout, {"next_page" : reverse_lazy('home')}, name='logout'),
)
