from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'zerg.views.index'),
    url(r'^data/', 'zerg.views.data'),
)
