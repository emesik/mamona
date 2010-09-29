from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from django.contrib.sites.models import Site

from mamona.models import Payment
from mamona.utils import get_backend_settings

def confirm(request, payment_id):
	payment = get_object_or_404(Payment, id=payment_id, status='in_progress', backend='paypal')
	paypal = get_backend_settings('paypal')
	try:
		return_url = paypal['return_url']
	except KeyError:
		# TODO: use https when needed
		return_url = 'http://%s%s' % (
				Site.objects.get_current().domain,
				reverse('mamona-paypal-return', kwargs={'payment_id': payment.id})
				)
	notify_url = 'http://%s%s' % (
			Site.objects.get_current().domain,
			reverse('mamona-paypal-ipn')
			)
	return direct_to_template(
			request,
			'mamona/backends/paypal/confirm.html',
			{
				'payment': payment, 'paypal': paypal,
				'return_url': return_url, 'notify_url': notify_url
				}
			)

def return_from_gw(request, payment_id):
	payment = get_object_or_404(Payment, id=payment_id)
	return direct_to_template(
			request,
			'mamona/backends/paypal/return.html',
			{'payment': payment}
			)

def ipn(request):
	data = request.POST.copy()
	payment = get_object_or_404(Payment, id=data['invoice'], status='in_progress', backend='paypal')
	data['_cmd'] = '_notify-validate'

	udata = urlencode(data)
	r = urllib2.Request(get_backend_settings('paypal')['url'])
	r.add_header("Content-type", "application/x-www-form-urlencoded")
	h = urllib2.urlopen(r, udata)
	result = h.read()
	h.close()

	if result == "VERIFIED":
		# TODO: save foreign-id from data['txn_id']
		return HttpResponseRedirect(payment.on_success())
	else:
		# XXX: marking the payment as failed would create a security hole
		return HttpResponseNotFound()
