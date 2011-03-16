from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _
from models import Payment
from utils import get_backend_choices

class PaymentMethodForm(forms.Form):
	"""Shows choice field with all active payment backends. You may use it with
	existing Payment instance to push it through all the remaining logic, getting
	the link to the next payment step from proceed_to_gateway() method."""
	backend = forms.ChoiceField(
			choices=get_backend_choices(),
			label=_("Payment method"),
			)

	def __init__(self, *args, **kwargs):
		self.payment = kwargs.pop('payment', None)
		super(PaymentMethodForm, self).__init__(*args, **kwargs)

	def save(self, payment=None):
		if not payment:
			payment = self.payment
		payment.backend = self.cleaned_data['backend']
		payment.save()


class ConfirmationForm(forms.Form):
	def __init__(self, *args, **kwargs):
		self.payment = kwargs.pop('payment')
		super(forms.Form, self).__init__(*args, **kwargs)
		self.payment.change_status('in_progress')
