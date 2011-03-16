from django import forms
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from ...forms import ConfirmationForm
from ...utils import get_backend_settings

class PaypalConfirmationForm(ConfirmationForm):
	invoice = forms.IntegerField(widget=forms.HiddenInput())
	first_name = forms.CharField(required=False, widget=forms.HiddenInput())
	last_name = forms.CharField(required=False, widget=forms.HiddenInput())
	email = forms.EmailField(required=False, widget=forms.HiddenInput())
	city = forms.CharField(required=False, widget=forms.HiddenInput())
	zip = forms.CharField(required=False, widget=forms.HiddenInput())
	country = forms.CharField(required=False, widget=forms.HiddenInput())
	amount = forms.DecimalField(widget=forms.HiddenInput())
	currency_code = forms.CharField(widget=forms.HiddenInput())
	notify_url = forms.CharField(required=False, widget=forms.HiddenInput())
	business = forms.EmailField(widget=forms.HiddenInput())
	cmd = forms.CharField(widget=forms.HiddenInput(), initial='_cart')
	upload = forms.CharField(widget=forms.HiddenInput(), initial='1')
	charset = forms.CharField(widget=forms.HiddenInput(), initial='utf-8')

	def __init__(self, *args, **kwargs):
		super(PaypalConfirmationForm, self).__init__(*args, **kwargs)
		# a keyword, haha :)
		self.fields['return'] = forms.CharField(widget=forms.HiddenInput())
		paypal = get_backend_settings('paypal')
		customer = self.payment.get_customer_data()
		self.fields['invoice'].initial = self.payment.pk
		self.fields['first_name'].initial = customer.get('first_name', '')
		self.fields['last_name'].initial = customer.get('last_name', '')
		self.fields['email'].initial = customer.get('email', '')
		self.fields['city'].initial = customer.get('city', '')
		self.fields['country'].initial = customer.get('country_iso', '')
		self.fields['zip'].initial = customer.get('postal_code', '')
		self.fields['amount'].initial = self.payment.amount
		self.fields['currency_code'].initial = self.payment.currency
		self.fields['return'].initial = paypal['url']
		self.fields['business'].initial = paypal['email']
		i = 1
		for item in self.payment.get_items():
			self.fields['item_name_%d' % i] = forms.CharField(widget=forms.HiddenInput())
			self.fields['item_name_%d' % i].initial = item['name']
			self.fields['amount_%d' % i] = forms.DecimalField(widget=forms.HiddenInput())
			self.fields['amount_%d' % i].initial = item['unit_price']
			self.fields['quantity_%d' % i] = forms.DecimalField(widget=forms.HiddenInput())
			self.fields['quantity_%d' % i].initial = item['quantity']
			i += 1
		try:
			self.fields['return'].initial = paypal['return_url']
		except KeyError:
			# TODO: use https when needed
			self.fields['return'].initial = 'http://%s%s' % (
					Site.objects.get_current().domain,
					reverse('mamona-paypal-return', kwargs={'payment_id': self.payment.id})
					)
		self.fields['notify_url'].initial = 'http://%s%s' % (
				Site.objects.get_current().domain,
				reverse('mamona-paypal-ipn')
				)

	def clean(self, *args, **kwargs):
		raise NotImplementedError("This form is not intended to be validated here.")
