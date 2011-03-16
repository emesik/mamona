from datetime import datetime
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import DummyConfirmationForm
from . import models

def get_confirmation_form(payment):
	return {'form': DummyConfirmationForm(payment=payment), 'method': 'get',
			'action': reverse('mamona-dummy-decide', kwargs={'payment_id': payment.id})}
