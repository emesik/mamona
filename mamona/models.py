from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from abstract_mixin import AbstractMixin
import signals

PAYMENT_STATUS_CHOICES = (
		('new', _("New")),
		('paid', _("Paid")),
		('failed', _("Failed")),
		('in_progress', _("In progress")),
		)

class PaymentFactory(models.Model, AbstractMixin):
	amount = models.DecimalField(decimal_places=4, max_digits=20)
	currency = models.CharField(max_length=3)
	status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='new')
	backend = models.CharField(max_length=30)
	created_on = models.DateTimeField(auto_now_add=True)
	paid_on = models.DateTimeField(blank=True, null=True, default=None)

	class Meta:
		abstract = True

	def change_status(self, new_status):
		old_status = self.status
		self.status = new_status
		self.save()
		signals.payment_status_changed.send(
				sender=self,
				old_status=old_status, new_status=new_status
				)

	def on_success(self):
		"Launched by backend when payment is successfully finished."
		self.paid_on = datetime.now()
		self.change_status('paid')
		urls = {}
		signals.return_urls_query.send(sender=self, urls=urls)
		return urls['success']

	def on_failure(self):
		"Launched by backend when payment fails."
		self.change_status('failed')
		urls = {}
		signals.return_urls_query.send(sender=self, urls=urls)
		return urls['failure']

	def get_items(self):
		"""Retrieves item list. Listeners must fill 'items' list with
		at least one item. Each item is expected to be a dictionary,
		containing at least 'name' element and optionally 'unit_price' and
		'quantity' elements. If not present, 'unit_price' and 'quantity'
		default to 0 and 1 respectively.

		Listener is responsible for providing data consistient with
		Payment.amount - otherwise the final amount may differ, depending
		on the backend used.
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
	class Payment(PaymentFactory.construct(order=order_class, **kwargs)):
		pass
	# XXX: put Payment at the top of our module to allow import in backends
	bknd_models_modules = import_backend_modules('models')
	for bknd_name, models in bknd_models_modules.items():
		app_cache.register_models(bknd_name, *models.build_models(Payment))
