from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render

from models import Payment, Order, payment_from_order
from forms import PaymentMethodForm
from urllib import urlencode
from urlparse import urlunparse

def process_order(request):
	"""This view should receive 'order_id' via POST, and optionally 'backend' too.
	It will use a signal to ask for filling in the payment details."""
	try:
		order = Order.objects.get(pk=request.POST['order_id'])
	except (Order.DoesNotExist, KeyError):
		return HttpResponseNotFound()
	payment = payment_from_order(order)
	payment.save()
	data = {}
	try:
		data['backend'] = request.POST['backend']
	except KeyError:
		pass
	url = reverse('mamona-process-payment', kwargs={'payment_id': payment.id})
	url = urlunparse((None, None, url, None, urlencode(data), None))
	return HttpResponseRedirect(url)

def process_payment(request, payment_id):
	"""This view processes the specified payment. It checks for backend, validates
	it's availability and asks again for it if something is wrong."""
	payment = get_object_or_404(Payment, id=payment_id, status='new')
	if request.method == 'POST' or request.REQUEST.has_key('backend'):
		data = request.REQUEST
	elif len(settings.MAMONA_ACTIVE_BACKENDS) == 1:
		data = {'backend': settings.MAMONA_ACTIVE_BACKENDS[0]}
	else:
		data = None
	bknd_form = PaymentMethodForm(data=data, payment=payment)
	if bknd_form.is_valid():
		bknd_form.save()
		return HttpResponseRedirect(
				reverse('mamona-confirm-payment', kwargs={'payment_id': payment.id}))
	return render(
			request,
			'mamona/select_payment_method.html',
			{'payment': payment, 'form': bknd_form},
			)

def confirm_payment(request, payment_id):
	payment = get_object_or_404(Payment, id=payment_id, status='new')
	formdata = payment.get_processor().get_confirmation_form(payment)
	return render(request, 'mamona/confirm.html',
			{'formdata': formdata, 'payment': payment})
