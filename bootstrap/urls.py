from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^$', 'bootstrap.views.home', name='home'),
)
