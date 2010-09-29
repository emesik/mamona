from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse

from datetime import datetime

def proceed_to_gateway(payment):
	# We need an intermediate step here, to gather data and POST it to PayPal
	return reverse('mamona-paypal-confirm', kwargs={'payment_id': payment.id})
