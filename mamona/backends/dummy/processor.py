from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import DummyTxn

from datetime import datetime

def proceed_to_gateway(payment):
	# An example how payment backend could create additional models related to Payment:
	print payment
	txn = DummyTxn.objects.create(
			payment=payment,
			comment="Dummy transaction created on %s" % datetime.now()
			)
	return reverse('mamona-dummy-decide', kwargs={'payment_id': payment.id})
