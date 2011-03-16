from datetime import datetime
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse

from mamona.utils import get_backend_settings

from . import forms

def proceed_to_gateway(payment):
	# We need an intermediate step here, to gather data and POST it to PayPal
	return reverse('mamona-paypal-confirm', kwargs={'payment_id': payment.id})

def get_confirmation_form(payment):
	paypal = get_backend_settings('paypal')
	form = forms.PaypalConfirmationForm(payment=payment)
	return {'form': form, 'method': 'post', 'action': paypal['url']}
