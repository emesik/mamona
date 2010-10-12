from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from abstract_mixin import AbstractMixin
import signals

PAYMENT_STATUS_CHOICES = (
		('new', _("New")),
		('in_progress', _("In progress")),
		('partially_paid', _("Partially paid")),
		('paid', _("Paid")),
		('failed', _("Failed")),
		)

class PaymentFactory(models.Model, AbstractMixin):
	amount = models.DecimalField(decimal_places=4, max_digits=20)
	currency = models.CharField(max_length=3)
	status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='new')
	backend = models.CharField(max_length=30)
	created_on = models.DateTimeField(auto_now_add=True)
	paid_on = models.DateTimeField(blank=True, null=True, default=None)
	amount_paid = models.DecimalField(decimal_places=4, max_digits=20, default=0)

	class Meta:
		abstract = True

	def change_status(self, new_status):
		"""Always change payment's status via this method. Otherwise the signal
		will not be emitted."""
		old_status = self.status
		self.status = new_status
		self.save()
		signals.payment_status_changed.send(
				sender=self,
				old_status=old_status, new_status=new_status
				)

	def on_payment(self, amount=None):
		"""Launched by backend when payment receives any new money. It defaults to
		complete payment, but can optionally accept received amount as a parameter
		to handle partial payments.
		"""
		self.paid_on = datetime.now()
		if amount:
			self.amount_paid = amount
		else:
			self.amount_paid = self.amount
		fully_paid = self.amount_paid >= self.amount
		if fully_paid:
			self.change_status('paid')
		else:
			self.change_status('partially_paid')
		urls = {}
		signals.return_urls_query.send(sender=self, urls=urls)
		if not fully_paid:
			try:
				# Applications do NOT have to define 'partially_paid' URL.
				return urls['partially_paid']
			except KeyError:
				pass
		return urls['paid']

	def on_failure(self):
		"Launched by backend when payment fails."
		self.change_status('failed')
		urls = {}
		signals.return_urls_query.send(sender=self, urls=urls)
		return urls['failure']

	def get_items(self):
		"""Retrieves item list using signal query. Listeners must fill
		'items' list with at least one item. Each item is expected to be
		a dictionary, containing at least 'name' element and optionally
		'unit_price' and 'quantity' elements. If not present, 'unit_price'
		and 'quantity' default to 0 and 1 respectively.

		Listener is responsible for providing item list with sum of prices
		consistient with Payment.amount. Otherwise the final amount may
		differ and lead to unpredictable results, depending on the backend used.
		"""
		items = []
		signals.order_items_query.send(sender=self, items=items)
		# XXX: sanitization and filling with defaults - do we need it? may be costly.
		if len(items) == 1 and not items[0].has_key('unit_price'):
			items[0]['unit_price'] = self.amount
			return items
		for item in items:
			assert item.has_key('name')
			if not item.has_key('unit_price'):
				item['unit_price'] = 0
			if not item.has_key('quantity'):
				item['quantity'] = 1
		return items

	def get_customer_data(self):
		"""Retrieves customer data. The default empty dictionary is
		already the minimal implementation.
		"""
		customer = {}
		signals.customer_data_query.send(sender=self, customer=customer)
		return customer

	@classmethod
	def contribute(cls, order, **kwargs):
		return {'order': models.ForeignKey(order, **kwargs)}

	def __unicode__(self):
		return u"%s payment of %s%s%s for %s" % (
				self.get_status_display(),
				self.amount,
				self.currency,
				u" on %s" % self.paid_on if self.status == 'paid' else "",
				self.order
				)

from django.db.models.loading import cache as app_cache
from utils import import_backend_modules
def build_payment_model(order_class, **kwargs):
	global Payment
	global Order
	class Payment(PaymentFactory.construct(order=order_class, **kwargs)):
		pass
	Order = order_class
	bknd_models_modules = import_backend_modules('models')
	for bknd_name, models in bknd_models_modules.items():
		app_cache.register_models(bknd_name, *models.build_models(Payment))

def payment_from_order(order):
	"""Builds payment based on given Order instance."""
	payment = Payment()
	signals.order_to_payment_query.send(sender=None, order=order, payment=payment)
	return payment
