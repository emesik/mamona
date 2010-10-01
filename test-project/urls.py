from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	(r'^mamona/', include('mamona.urls')),
	url(r'^$', 'sales.views.place_order', name='place-order'),
	url(r'^details/(?P<order_id>[0-9]+)/$', 'order.views.show_order', name='show-order'),
	# Uncomment the next line to enable the admin:
	#(r'^admin/', include(admin.site.urls)),
)
