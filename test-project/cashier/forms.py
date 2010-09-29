from django import forms
from mamona.forms import PaymentMethodForm
from models import Order

# FIXME: This does not work! We cannot inherit from ModelForm and mamona.forms.PaymentMethodForm
# (which is a subclass of forms.Form).
#
#class OrderForm(forms.ModelForm):
#	class Meta:
#		model = Order
#		fields = ('name', 'total')
#	
#OrderWithPaymentForm = model_form_with_payment(OrderForm)
#

class OrderForm(forms.Form):
	name = forms.CharField(max_length=100)
	total = forms.DecimalField(decimal_places=2, max_digits=8)

class OrderWithPaymentForm(OrderForm, PaymentMethodForm):
	pass
