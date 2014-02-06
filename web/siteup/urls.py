from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from siteup_frontend import views as fe_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'siteup.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', fe_views.HomeView.as_view(), name='home'),
    url(r'^login', fe_views.LoginView.as_view(), name="login"),
    url(r'^logout', fe_views.logout_view, name="logout"),
    url(r'^signup', fe_views.SignupView.as_view(), name="signup"),
    url(r'^admin/', include(admin.site.urls)),
)
