from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from models import Payment
from forms import PaymentMethodForm

def process_payment(request, payment_id):
	payment = get_object_or_404(Payment, id=payment_id, status='new')
	bknd_form = PaymentMethodForm(data=request.REQUEST, payment=payment)
	if not bknd_form.is_valid():
		return HttpResponseNotFound()
	return HttpResponseRedirect(bknd_form.proceed_to_gateway())
