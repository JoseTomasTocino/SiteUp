from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from siteup_frontend import views as fe_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'siteup.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', fe_views.HomeView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
)
