from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template

from models import Payment
from forms import PaymentMethodForm

def process_payment(request, payment_id):
	payment = get_object_or_404(Payment, id=payment_id, status='new')
	if request.method == 'POST' or request.REQUEST.has_key('backend'):
		data = request.REQUEST
	else:
		data = None
	bknd_form = PaymentMethodForm(data=data, payment=payment)
	if not bknd_form.is_valid():
		return direct_to_template(
				request,
				'mamona/base_confirm.html',
				{'payment': payment, 'form': bknd_form},
				)
	return HttpResponseRedirect(bknd_form.proceed_to_gateway())
