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
		self.payment = kwargs.pop('payment')
		super(PaymentMethodForm, self).__init__(*args, **kwargs)

	def proceed_to_gateway(self, payment=None):
		"""Saves backend information in the payment object, marks it as \"In progress\"
		and returns an URL to the next payment step.
		
		It can get the payment object directly as a parameter or use the object passed
		before to the class constructor.
		"""
		if payment is None:
			payment = self.payment
		if payment:
			payment.backend = self.cleaned_data['backend']
			payment.change_status('in_progress')
		else:
			raise ValueError, _("Payment object is not set. Cannot proceed to the gateway.")
		return payment.get_processor().proceed_to_gateway(payment)

	def save(self):
		self.payment.backend = self.cleaned_data['backend']
		self.payment.save()


class ConfirmationForm(forms.Form):
	def __init__(self, *args, **kwargs):
		self.payment = kwargs.pop('payment')
		super(forms.Form, self).__init__(*args, **kwargs)
		self.payment.change_status('in_progress')
