from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from mamona import signals

def return_urls_query_listener(sender, instance=None, urls=None, **kwargs):
	url = 'http://%s%s' % (
			Site.objects.get_current().domain,
			reverse('show-order', kwargs={'order_id': instance.order.id})
			)
	urls.update({'paid': url, 'failure': url})

def order_items_query_listener(sender, instance=None, items=None, **kwargs):
	for item in instance.order.item_set.all():
		items.append({'name': item.name, 'unit_price': item.price})

def payment_status_changed_listener(sender, instance=None, old_status=None, new_status=None, **kwargs):
	if new_status == 'paid':
		instance.order.status = 's'
		instance.order.save()
	elif new_status == 'failed':
		instance.order.status = 'f'
		instance.order.save()
	elif new_status == 'partially_paid':
		instance.order.status = 'p'
		instance.order.save()

def order_to_payment_listener(sender, order=None, payment=None, **kwargs):
	payment.order = order
	payment.amount = order.total
	payment.currency = order.currency

signals.payment_status_changed.connect(payment_status_changed_listener)
signals.order_items_query.connect(order_items_query_listener)
signals.return_urls_query.connect(return_urls_query_listener)
signals.order_to_payment_query.connect(order_to_payment_listener)
