from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404

from mamona.forms import PaymentMethodForm
from order.models import UnawareOrder
from forms import ItemFormSet

import random

def order_singleitem(request):
	# approach 1: single item purchase with predefined backend
	order = UnawareOrder.objects.create()
	order.item_set.create(
			name=u"Donation for Mamona author",
			price=random.random() * 8 + 2
			)
	return direct_to_template(
			request,
			'sales/order_singleitem.html',
			{'order': order, 'backend': 'paypal'}
			)

def order_multiitem(request):
	# approach 2: an order with no payment method (Mamona will ask)
	order = UnawareOrder()
	if request.method == 'POST':
		formset = ItemFormSet(instance=order, data=request.POST)
		if formset.is_valid():
			order.save()
			formset.save()
			payment = order.payments.create(amount=order.total, currency=order.currency)
			return HttpResponseRedirect(
					reverse('mamona-process-payment', kwargs={'payment_id': payment.id})
					)
	else:
		formset = ItemFormSet(instance=order)
	return direct_to_template(
		request,
		'sales/order_multiitem.html',
		{'order': order, 'formset': formset}
		)

def order_singlescreen(request):
	# approach 3: single screen (ask for everything)
	order = UnawareOrder()
	payment_form = PaymentMethodForm(data=request.POST or None)
	formset = ItemFormSet(instance=order, data=request.POST or None)
	if request.method == 'POST':
		if formset.is_valid() and payment_form.is_valid():
			order.save()
			formset.save()
			payment = order.payments.create(amount=order.total, currency=order.currency)
			payment_form.save(payment)
			return HttpResponseRedirect(
					reverse('mamona-confirm-payment', kwargs={'payment_id': payment.id}))
	return direct_to_template(
		request,
		'sales/order_singlescreen.html',
		{'order': order, 'formset': formset, 'payment_form': payment_form}
		)
