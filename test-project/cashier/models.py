from django.db import models
from mamona.models import build_payment_model

from decimal import Decimal

class Order(models.Model):
	name = models.CharField(max_length=100)
	total = models.DecimalField(decimal_places=2, max_digits=8)
	status = models.CharField(
			max_length=1,
			choices=(('s','s'), ('f','f')),
			blank=True, null=True,
			default=None
			)

	def __unicode__(self):
		return self.name

	def checkout(self):
		return self.payments.create(amount=self.total, currency='EUR')

	def on_payment_success(self):
		self.status = 's'
		self.save()

	def on_payment_failure(self):
		self.status = 'f'
		self.save()

Payment = build_payment_model(Order, unique=False, related_name='payments')
