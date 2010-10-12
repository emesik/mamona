# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse

from decimal import Decimal

class UnawareOrder(models.Model):
	"""This is an example of order model, which is unaware of
	Mamona existence.
	"""
	total = models.DecimalField(decimal_places=2, max_digits=8, default=0)
	currency = models.CharField(max_length=3, default='EUR')
	status = models.CharField(
			max_length=1,
			choices=(('s','success'), ('f','failure'), ('p', 'partially paid')),
			blank=True,
			default=''
			)

	def name(self):
		if self.item_set.count() == 0:
			return u"Empty order"
		elif self.item_set.count() == 1:
			return self.item_set.all()[0].name
		else:
			return u"Multiple-item order"

	def recalculate_total(self):
		total = Decimal('0')
		for item in self.item_set.all():
			total += item.price
		self.total = total
		self.save()

class Item(models.Model):
	"""Basic order item.
	"""
	order = models.ForeignKey(UnawareOrder)
	name = models.CharField(max_length=20)
	price = models.DecimalField(decimal_places=2, max_digits=8)

	def __unicode__(self):
		return self.name

def recalculate_total(sender, instance, **kwargs):
	instance.order.recalculate_total()
models.signals.post_save.connect(recalculate_total, sender=Item)
