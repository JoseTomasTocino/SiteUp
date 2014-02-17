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
    url(r'^groups/edit/(?P<pk>\d{1,})', fe_views.GroupUpdateView.as_view(), name="edit_group"),
    url(r'^groups/activate/(?P<pk>\d{1,})', fe_views.GroupActivateView.as_view(), name="activate_group"),
    url(r'^groups/deactivate/(?P<pk>\d{1,})', fe_views.GroupDeactivateView.as_view(), name="deactivate_group"),
    url(r'^groups/delete/(?P<pk>\d{1,})', fe_views.GroupDeleteView.as_view(), name="delete_group"),
    url(r'^groups/(?P<pk>\d{1,})/addcheck', fe_views.ChooseCheckTypeTemplateView.as_view(), name="new_check"),
    url(r'^groups/(?P<pk>\d{1,})/addpingcheck', fe_views.PingCheckCreateView.as_view(), name="new_ping_check"),
    url(r'^groups/(?P<pk>\d{1,})/adddnscheck', fe_views.DnsCheckCreateView.as_view(), name="new_dns_check"),
    url(r'^groups/(?P<pk>\d{1,})/addportcheck', fe_views.PortCheckCreateView.as_view(), name="new_port_check"),
    url(r'^groups/(?P<pk>\d{1,})/addhttpcheck', fe_views.HttpCheckCreateView.as_view(), name="new_http_check"),

    url(r'^checks/delete/(?P<type>\w{1,})/(?P<pk>\d{1,})', fe_views.CheckDeleteView.as_view(), name="delete_check"),
)
