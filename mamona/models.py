from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from abstract_mixin import AbstractMixin

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

	def on_success(self):
		"Launched by backend when payment is successfully finished."
		self.status = 'paid'
		self.paid_on = datetime.now()
		self.save()
		return self.order.on_payment_success()

	def on_failure(self):
		"Launched by backend when payment fails."
		self.status = 'failed'
		self.save()
		return self.order.on_payment_failure()

	def get_items_list(self):
		"""Retrieves item list from order object.
		The order object must provide method of the same name,
		which must return at least one item. Each item is expected
		to be a dictionary, containing at least 'name' element and
		optionally 'price' element.
		"""
		return self.order.get_items_list()

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

Payment = None

from django.db.models.loading import cache as app_cache
from utils import import_backend_modules
def build_payment_model(order_class, **kwargs):
	class Payment(PaymentFactory.construct(order=order_class, **kwargs)):
		pass
	# XXX: put Payment at the top of our module to allow import in backends
	global Payment
	bknd_models_modules = import_backend_modules('models')
	for bknd_name, models in bknd_models_modules.items():
		app_cache.register_models(bknd_name, *models.build_models(Payment))
