from datetime import datetime
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse

from mamona.utils import get_backend_settings

from . import forms

def get_confirmation_form(payment):
	paypal = get_backend_settings('paypal')
	form = forms.PaypalConfirmationForm(payment=payment)
	return {'form': form, 'method': 'post', 'action': paypal['url']}
