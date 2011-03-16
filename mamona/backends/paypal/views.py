from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _

from mamona.models import Payment
from mamona.utils import get_backend_settings
from mamona.signals import return_urls_query

import urllib2
from urllib import urlencode
from decimal import Decimal

def return_from_gw(request, payment_id):
	payment = get_object_or_404(Payment, id=payment_id)
	urls = {}
	return_urls_query.send(sender=payment, urls=urls)
	if payment.status == 'failed':
		return HttpResponseRedirect(urls['failure'])
	elif payment.status == 'paid':
		return HttpResponseRedirect(urls['paid'])
	elif payment.status == 'partially_paid':
		try:
			return HttpResponseRedirect(urls['partially_paid'])
		except KeyError:
			return HttpResponseRedirect(urls['paid'])
	return direct_to_template(
			request,
			'mamona/base_return.html',
			{'payment': payment}
			)

@csrf_exempt
def ipn(request):
	"""Instant Payment Notification callback.
	See https://cms.paypal.com/us/cgi-bin/?&cmd=_render-content&content_ID=developer/e_howto_admin_IPNIntro
	for details."""
	# TODO: add some logging here, as all the errors will occur silently
	payment = get_object_or_404(Payment, id=request.POST['invoice'], status='in_progress', backend='paypal')
	data = list(request.POST.items())
	data.insert(0, ('cmd', '_notify-validate'))
	udata = urlencode(data)
	url = get_backend_settings('paypal')['url']
	r = urllib2.Request(url)
	r.add_header("Content-type", "application/x-www-form-urlencoded")
	h = urllib2.urlopen(r, udata)
	result = h.read()
	h.close()

	if result == "VERIFIED":
		# TODO: save foreign-id from data['txn_id']
		amount = Decimal(request.POST['mc_gross'])
		payment.on_payment(amount)
		return HttpResponse('OKTHXBAI')
	else:
		# XXX: marking the payment as failed would create a security hole
		return HttpResponseNotFound()
