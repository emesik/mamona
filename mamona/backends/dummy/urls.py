from django.conf.urls.defaults import *

urlpatterns = patterns('mamona.backends.dummy.views',
	url(r'^decide/(?P<payment_id>[0-9]+)/$', 'decide_success_or_failure', name='mamona-dummy-decide'),
	url(r'^success/(?P<payment_id>[0-9]+)/$', 'on_payment_success', name='mamona-dummy-on-success'),
	url(r'^failure/(?P<payment_id>[0-9]+)/$', 'on_payment_failure', name='mamona-dummy-on-failure'),
)
