from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from mamona.models import Payment
from mamona.utils import get_backend_settings
from mamona.signals import return_urls_query

import urllib2
from urllib import urlencode
from decimal import Decimal

def return_from_gw(request, payment_id):
	payment = get_object_or_404(Payment, id=payment_id)
	urls = {}
	return_urls_query.send(sender=None, instance=payment, urls=urls)
	if payment.status == 'failed':
		return HttpResponseRedirect(urls['failure'])
	elif payment.status == 'paid':
		return HttpResponseRedirect(urls['paid'])
	elif payment.status == 'partially_paid':
		try:
			return HttpResponseRedirect(urls['partially_paid'])
		except KeyError:
			return HttpResponseRedirect(urls['paid'])
	return render(
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
	try:
		payment = get_object_or_404(Payment, id=request.POST['invoice'],
				status__in=('in_progress', 'partially_paid', 'paid', 'failed'),
				backend='paypal')
	except (KeyError, ValueError):
		return HttpResponseBadRequest()
	charset = request.POST.get('charset', 'UTF-8')
	request.encoding = charset
	data = request.POST.dict()
	data['cmd'] = '_notify-validate'

	# Encode data as PayPal wants it.
	for k, v in data.items():
		data[k] = v.encode(charset)

	udata = urlencode(data)
	url = get_backend_settings('paypal')['url']
	r = urllib2.Request(url)
	r.add_header("Content-type", "application/x-www-form-urlencoded")
	h = urllib2.urlopen(r, udata)
	result = h.read()
	h.close()

	if result == "VERIFIED":
		# TODO: save foreign-id from data['txn_id']
		if payment.status == 'in_progress':
			amount = Decimal(request.POST['mc_gross'])
			# TODO: handle different IPN calls, e.g. refunds
			payment.on_payment(amount)
		return HttpResponse('OKTHXBAI')
	else:
		# XXX: marking the payment as failed would create a security hole
		return HttpResponseNotFound()
