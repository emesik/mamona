from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404

from mamona.forms import PaymentMethodForm
from order.models import UnawareOrder
from forms import ItemFormSet

def place_order(request):
	order = UnawareOrder()
	if request.method == 'POST':
		form = PaymentMethodForm(data=request.POST)
		formset = ItemFormSet(data=request.POST)
		if form.is_valid() and formset.is_valid():
			order.save()
			for f in formset.forms:
				f.instance.order = order
				f.save()
			payment = order.payments.create(amount=order.total, currency='EUR')
			next_step = form.proceed_to_gateway(payment)
			return HttpResponseRedirect(next_step)
	else:
		form = PaymentMethodForm()
		formset = ItemFormSet()
	return direct_to_template(
		request,
		'sales/place_order.html',
		{'form': form, 'formset': formset}
		)
