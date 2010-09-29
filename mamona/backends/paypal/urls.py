from django.conf.urls.defaults import *

urlpatterns = patterns('mamona.backends.paypal.views',
	url(r'^confirm/(?P<payment_id>[0-9]+)/$', 'confirm', name='mamona-paypal-confirm'),
	url(r'^return/(?P<payment_id>[0-9]+)/$', 'return_from_gw', name='mamona-paypal-return'),
	url(r'^ipn/$', 'ipn', name='mamona-paypal-ipn'),
)
