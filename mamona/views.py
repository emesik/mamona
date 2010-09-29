from django.conf import settings
from django.http import HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from models import Payment

def process_payment(request, payment_id):
	if request.method != 'POST':
		return HttpResponseNotAllowed(['POST'])
	backend_name = request.REQUEST.get('backend')
	if backend_name not in settings.MAMONA_BACKENDS:
		return HttpResponseNotFound()
	payment = get_object_or_404(Payment, id=payment_id, status='new')
	mamona = __import__('mamona.backends.%s.views' % backend_name)
	payment.status = 'in_progress'
	payment.backend = backend_name
	payment.save()
	backend_process_payment = getattr(mamona.backends, backend_name).views.process_payment
	return backend_process_payment(request, payment)
