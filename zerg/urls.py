from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'zerg.views.index'),
    url(r'^world/([\[\]\'a-zA-Z_]+)$', 'zerg.views.world'),
    url(r'^data/(\d+)$', 'zerg.views.data'),
)
