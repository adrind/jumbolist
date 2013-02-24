from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'jlist.views.load_home', name='home'),
     url(r'^signup/$', 'jlist.views.register', name='register'),
     url(r'^login/$', 'jlist.views.login_attempt', name='login_attempt'),
     url(r'^profile/$', 'jlist.views.profile', name='profile'),
     url(r'^sell/$', 'jlist.views.sellers_page', name='sellers'),
     url(r'^additem/$', 'jlist.views.additem', name='add'),
     url(r'^manage/$', 'jlist.views.manage', name='manage'),
     url(r'^additem/$', 'jlist.views.add', name='add'),
    url(r'^displayItems/$', 'jlist.views.display_items', name='display_items'),




    # url(r'^jumbolist/', include('jumbolist.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
