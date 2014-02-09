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
    url(r'^profile', fe_views.ProfileView.as_view(), name="profile"),
    url(r'^dashboard', fe_views.DashboardView.as_view(), name="dashboard"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^groups/new', fe_views.GroupCreateView.as_view(), name="new_group"),
    url(r'^groups/(?P<pk>\d{1,})/addcheck', fe_views.CheckCreateView.as_view(), name="new_check"),
    url(r'^groups/edit/(?P<pk>\d{1,})', fe_views.GroupUpdateView.as_view(), name="edit_group"),
)
