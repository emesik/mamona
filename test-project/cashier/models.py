# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
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

	def get_items(self):
		"""An example of the minimal implementation."""
		return [{'name': self.name}]

	def get_customer_data(self):
		"""An example of the implementation.
		The minimal option is just an empty dictionary.
		"""
		return {
			'first_name': u"Grzegorz",
			'last_name': u"Brzęczyszczykiewicz",
			'city': u"Łękołowy",
			'country_name': u"Poland",
			'country_iso': 'pl',
			}

	def checkout(self):
		return self.payments.create(amount=self.total, currency='EUR')

Payment = build_payment_model(Order, unique=False, related_name='payments')

import listeners
