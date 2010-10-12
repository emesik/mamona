from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r'^mamona/', include('mamona.urls')),
	url(r'^$', 'sales.views.order_1click', name='sales-order-1click'),
	url(r'^multiitem$', 'sales.views.order_multiitem', name='sales-order-multiitem'),
	url(r'^singlescreen$', 'sales.views.order_singlescreen', name='sales-order-singlescreen'),
	url(r'^details/(?P<order_id>[0-9]+)/$', 'order.views.show_order', name='show-order'),
)
