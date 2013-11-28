from django.conf.urls import patterns, url

urlpatterns = patterns('',
    (r'$', 'zerg.views.index'),
)
