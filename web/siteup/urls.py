from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from siteup_frontend import views as fe_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'siteup.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', fe_views.HomeView.as_view(), name='home'),
    url(r'^login$', fe_views.LoginView.as_view(), name="login"),
    url(r'^logout$', fe_views.LogoutView.as_view(), name="logout"),
    url(r'^password_reset$', fe_views.password_reset, name="password_reset"),
    url(r'^password_reset_done$', fe_views.password_reset_done, name="password_reset_done"),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', fe_views.password_reset_confirm, name="password_reset_confirm"),
    url(r'^password_reset_complete/$', fe_views.password_reset_complete, name="password_reset_complete"),

    url(r'^signup/$', fe_views.SignupView.as_view(), name="signup"),
    url(r'^changepassword/$', fe_views.ChangePasswordView.as_view(), name="changepassword"),

    url(r'^profile', fe_views.ProfileView.as_view(), name="profile"),
    url(r'^dashboard', fe_views.DashboardView.as_view(), name="dashboard"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^groups/new', fe_views.GroupCreateView.as_view(), name="new_group"),
    url(r'^groups/edit/(?P<pk>\d{1,})', fe_views.GroupUpdateView.as_view(), name="edit_group"),
    url(r'^groups/enable/(?P<pk>\d{1,})', fe_views.GroupEnableView.as_view(), name="enable_group"),
    url(r'^groups/disable/(?P<pk>\d{1,})', fe_views.GroupDisableView.as_view(), name="disable_group"),
    url(r'^groups/delete/(?P<pk>\d{1,})', fe_views.GroupDeleteView.as_view(), name="delete_group"),

    url(r'^groups/(?P<pk>\d{1,})/addcheck/$', fe_views.ChooseCheckTypeTemplateView.as_view(), name="new_check"),
    url(r'^groups/(?P<pk>\d{1,})/addcheck/(?P<type>\w{1,})/$', fe_views.CheckCreateView.as_view(), name="new_check_next"),
    # url(r'^groups/(?P<pk>\d{1,})/addpingcheck', fe_views.PingCheckCreateView.as_view(), name="new_ping_check"),
    # url(r'^groups/(?P<pk>\d{1,})/adddnscheck', fe_views.DnsCheckCreateView.as_view(), name="new_dns_check"),
    # url(r'^groups/(?P<pk>\d{1,})/addportcheck', fe_views.PortCheckCreateView.as_view(), name="new_port_check"),
    # url(r'^groups/(?P<pk>\d{1,})/addhttpcheck', fe_views.HttpCheckCreateView.as_view(), name="new_http_check"),

    url(r'^checks/edit/(?P<type>\w{1,})/(?P<pk>\d{1,})/$', fe_views.CheckUpdateView.as_view(), name="edit_check"),
    url(r'^checks/delete/(?P<type>\w{1,})/(?P<pk>\d{1,})/$', fe_views.CheckDeleteView.as_view(), name="delete_check"),
    url(r'^checks/enable/(?P<type>\w{1,})/(?P<pk>\d{1,})/$', fe_views.CheckEnableView.as_view(), name="enable_check"),
    url(r'^checks/disable/(?P<type>\w{1,})/(?P<pk>\d{1,})/$', fe_views.CheckDisableView.as_view(), name="disable_check"),
    url(r'^checks/(?P<type>\w{1,})/(?P<pk>\d{1,})/$', fe_views.CheckDetailView.as_view(), name="view_check"),

)
