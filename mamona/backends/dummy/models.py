from django.db import models

from mamona.abstract_mixin import AbstractMixin

class DummyTxnFactory(models.Model, AbstractMixin):
	comment = models.CharField(max_length=100, default="a dummy transaction")

	class Meta:
		abstract = True

	@classmethod
	def contribute(cls, payment):
		return {'payment': models.ForeignKey(payment)}


def build_models(payment_class):
	class DummyTxn(DummyTxnFactory.construct(payment_class)):
		pass
	return [DummyTxn]
