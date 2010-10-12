from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from order.models import UnawareOrder
from mamona.models import Payment

from decimal import Decimal
from random import randint

class SimpleTest(TestCase):
	fixtures = ['site']

	def setUp(self):
		self.o1 = UnawareOrder.objects.create(total=Decimal("25.12"))
		i = 1
		while i <= randint(1,10):
			self.o1.item_set.create(
					name="Item %s" % i,
					price=Decimal(randint(1,100))/Decimal("100")
					)
			i += 1
		self.o2 = UnawareOrder.objects.create(total=Decimal("0.01"))
		i = 1
		while i <= randint(1,10):
			self.o2.item_set.create(
					name="Item %s" % i,
					price=Decimal(randint(1,100))/Decimal("100")
					)
			i += 1
		self.o3 = UnawareOrder.objects.create(total=Decimal("0.01"))
		i = 1
		while i <= randint(1,10):
			self.o3.item_set.create(
					name="Item %s" % i,
					price=Decimal(randint(1,100))/Decimal("100")
					)
			i += 1

	def test_payment_creation(self):
		self.o1.payments.create(amount=self.o1.total)
		self.o2.payments.create(amount=self.o2.total)

	def test_payment_success_and_failure(self):
		p1 = self.o1.payments.create(amount=self.o1.total)
		p2 = self.o2.payments.create(amount=self.o2.total)
		p3 = self.o3.payments.create(amount=self.o2.total)
		p1.on_payment()
		self.assertEqual(p1.status, 'paid')
		self.assertEqual(self.o1.status, 's')
		p2.on_payment(p2.amount - Decimal('0.01'))
		self.assertEqual(p2.status, 'partially_paid')
		self.assertEqual(self.o2.status, 'p')
		p3.on_failure()
		self.assertEqual(p3.status, 'failed')
		self.assertEqual(self.o3.status, 'f')

	def test_dummy_backend(self):
		p1 = self.o1.payments.create(amount=self.o1.total)
		# request without backend should give us a form
		response = self.client.post(
				reverse('mamona-process-payment', kwargs={'payment_id': p1.id}),
				follow=True
				)
		self.assertEqual(response.status_code, 200)
		# this should succeed
		response = self.client.post(
				reverse('mamona-process-payment', kwargs={'payment_id': p1.id}),
				{'backend': 'dummy'},
				follow=True
				)
		p1 = Payment.objects.get(id=p1.id)
		self.assertEqual(p1.status, 'in_progress')
		# calling again should fail with 404, as the payment is marked 'in_progress'
		response = self.client.post(
				reverse('mamona-process-payment', kwargs={'payment_id': p1.id}),
				{'backend': 'dummy'},
				follow=True
				)
		self.assertEqual(response.status_code, 404)
		# choose success
		response = self.client.get(
				reverse('mamona-dummy-do-success', kwargs={'payment_id': p1.id}),
				follow=True
				)
		p1 = Payment.objects.get(id=p1.id)
		self.assertEqual(p1.status, 'paid')
		self.assertEqual(
				p1.amount,
				sum(map(lambda i: i.price, self.o1.item_set.all()))
				)
		# re-processing should fail
		response = self.client.post(
				reverse('mamona-process-payment', kwargs={'payment_id': p1.id}),
				{'backend': 'dummy'},
				follow=True
				)
		self.assertEqual(response.status_code, 404)
		# dummy backend should have created it's own model instance
		self.assertEqual(p1.dummytxn.payment_id, p1.id)

		p2 = self.o2.payments.create(amount=self.o2.total)
		# this should fail with 404
		response = self.client.get(
				reverse('mamona-dummy-do-success', kwargs={'payment_id': p2.id}),
				follow=True
				)
		self.assertEqual(response.status_code, 404)
		response = self.client.post(
				reverse('mamona-process-payment', kwargs={'payment_id': p2.id}),
				{'backend': 'dummy'},
				follow=True
				)
		response = self.client.get(
				reverse('mamona-dummy-do-failure', kwargs={'payment_id': p2.id}),
				follow=True
				)
		p2 = Payment.objects.get(id=p2.id)
		self.assertEqual(p2.status, 'failed')
		self.assertEqual(
				p2.amount,
				sum(map(lambda i: i.price, self.o2.item_set.all()))
				)
