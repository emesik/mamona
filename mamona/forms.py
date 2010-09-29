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

	def __init__(self, payment=None, *args, **kwargs):
		super(PaymentMethodForm, self).__init__(*args, **kwargs)
		self.payment = payment

	def proceed_to_gateway(self, payment=None):
		"""Saves backend information in the payment object, marks it as \"In progress\"
		and returns an URL to the next payment step.
		
		It can get the payment object directly as a parameter or use the object passed
		before to the class constructor.
		"""
		if payment is None:
			payment = self.payment
		if payment:
			payment.status = 'in_progress'
			payment.backend = self.cleaned_data['backend']
			payment.save()
		else:
			raise ValueError, _("Payment object is not set. Cannot proceed to the gateway.")
		mamona = __import__('mamona.backends.%s.processor' % payment.backend)
		return getattr(mamona.backends, payment.backend).processor.proceed_to_gateway(payment)


#def model_form_with_payment(model_form_class):
#	"""Returns a form class which inherits from model_form_class given as parameter
#	and PaymentMethodForm. This is useful when creating ModelForm for your Order model
#	merged together with payment method selection. If you do it directly, like...
#
#		class MyOrderForm(forms.ModelForm, PaymentMethodForm):
#			pass
#
#	...it will fail with metaclass conflict. This function resolves the conflict by
#	creating an intermediate metaclass.
#	"""
#
#	class NC_Meta(PaymentMethodForm.__metaclass__, model_form_class.__metaclass__):
#		pass
#	class OrderWithPaymentForm(PaymentMethodForm, model_form_class):
#		__metaclass__ = NC_Meta
#	OrderWithPaymentForm.Meta.fields = model_form_class.Meta.fields + ('backend',)
#	return OrderWithPaymentForm
