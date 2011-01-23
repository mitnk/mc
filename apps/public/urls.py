from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'apps.public.views.index'),
    (r'^category/$', 'apps.public.views.get_all_categories'),
    (r'^article/(\d+)/$', 'apps.public.views.get_article'),
    (r'^category/(\d+)/$', 'apps.public.views.get_category'),
    (r'^about/$', 'apps.public.views.about'),
)
