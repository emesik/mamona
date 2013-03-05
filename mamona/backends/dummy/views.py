from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from mamona.models import Payment
from models import DummyTxn

def decide_success_or_failure(request, payment_id):
	payment = get_object_or_404(Payment, id=payment_id, status='in_progress', backend='dummy')
	return render(
		request,
		'mamona/backends/dummy/decide.html',
		{'payment': payment}
		)

def do_payment_success(request, payment_id):
	payment = get_object_or_404(Payment, id=payment_id, status='in_progress', backend='dummy')
	return HttpResponseRedirect(payment.on_payment())

def do_payment_failure(request, payment_id):
	payment = get_object_or_404(Payment, id=payment_id, status='in_progress', backend='dummy')
	return HttpResponseRedirect(payment.on_failure())
