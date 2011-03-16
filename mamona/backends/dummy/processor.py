from datetime import datetime
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from mamona.forms import ConfirmationForm
from . import models

def proceed_to_gateway(payment):
	# An example how payment backend could create additional models related to Payment:
	txn = DummyTxn.objects.create(
			payment=payment,
			comment="Dummy transaction created on %s" % datetime.now()
			)
	return reverse('mamona-dummy-decide', kwargs={'payment_id': payment.id})

def get_confirmation_form(payment):
	return {'form': ConfirmationForm(payment=payment), 'method': 'get',
			'action': reverse('mamona-dummy-decide', kwargs={'payment_id': payment.id})}
