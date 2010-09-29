from django.test import TestCase
from django.core.urlresolvers import reverse
from models import Order
from mamona.models import Payment

from decimal import Decimal

class SimpleTest(TestCase):
	def setUp(self):
		self.o1 = Order.objects.create(name="Order 1", total=Decimal("25.12"))
		self.o2 = Order.objects.create(name="Order 2", total=Decimal("0.01"))

	def test_payment_creation(self):
		self.o1.checkout()
		self.o2.checkout()
		self.o2.checkout()

	def test_payment_success_and_failure(self):
		p1 = self.o1.checkout()
		p2 = self.o2.checkout()
		p1.on_success()
		self.assertEqual(p1.status, 'paid')
		self.assertEqual(self.o1.status, 's')
		p2.on_failure()
		self.assertEqual(p2.status, 'failed')
		self.assertEqual(self.o2.status, 'f')

	def test_dummy_backend(self):
		p1 = self.o1.checkout()
		# GET should fail with 503
		response = self.client.get(
				reverse('mamona-process-payment', kwargs={'payment_id': p1.id}),
				follow=True
				)
		self.assertEqual(response.status_code, 405)
		# request without backend should fail with 404
		response = self.client.post(
				reverse('mamona-process-payment', kwargs={'payment_id': p1.id}),
				follow=True
				)
		self.assertEqual(response.status_code, 404)
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
				reverse('mamona-dummy-on-success', kwargs={'payment_id': p1.id}),
				follow=True
				)
		p1 = Payment.objects.get(id=p1.id)
		self.assertEqual(p1.status, 'paid')
		# re-processing should fail
		response = self.client.post(
				reverse('mamona-process-payment', kwargs={'payment_id': p1.id}),
				{'backend': 'dummy'},
				follow=True
				)
		self.assertEqual(response.status_code, 404)

		p2 = self.o2.checkout()
		# this should fail with 404
		response = self.client.get(
				reverse('mamona-dummy-on-success', kwargs={'payment_id': p2.id}),
				follow=True
				)
		self.assertEqual(response.status_code, 404)
		response = self.client.post(
				reverse('mamona-process-payment', kwargs={'payment_id': p2.id}),
				{'backend': 'dummy'},
				follow=True
				)
		response = self.client.get(
				reverse('mamona-dummy-on-failure', kwargs={'payment_id': p2.id}),
				follow=True
				)
		p2 = Payment.objects.get(id=p2.id)
		self.assertEqual(p2.status, 'failed')
