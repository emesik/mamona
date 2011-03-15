from django.dispatch import Signal

payment_status_changed = Signal(providing_args=['old_status', 'new_status'])
payment_status_changed.__doc__ = """
Sent when Payment status changes.
	old_status:	str
	new_status:	str
"""

order_items_query = Signal(providing_args=['items'])
order_items_query.__doc__ = """
Sent to ask for order's items.
	items:			list
Listeners must fill the items list with at least one item.
Each item must be a dict instance, with at least 'name' element defined.
Other accepted keys are 'quantity' and 'unit_price' which default to 1 and 0
respectively.
"""

customer_data_query = Signal(providing_args=['customer'])
customer_data_query.__doc__ = """
Sent to ask for customer's data.
	customer:		dict
Handling of this signal will depend on the gateways you want to enable.
Currently, with PayPal, it doesn't have to be answered at all.
The optional arguments accepted by paypal backend are:
first_name, last_name, email, city, postal_code, country_iso
"""

return_urls_query = Signal(providing_args=['urls'])
return_urls_query.__doc__ = """
Sent to ask for URLs to return from payment gateway.
	urls:			dict
Listeners must fill urls with at least two elements: 'paid' and 'failure',
which represent the URLs to return after paid and failed payment respectively.
The optional element 'partially_paid' is used to return after payment which
received incomplete amount.
"""

order_to_payment_query = Signal(providing_args=['order', 'payment'])
order_to_payment_query.__doc__ = """
Sent to ask for filling Payment object with order data:
	order:			order instance
	payment:		Payment instance
It needs to be answered only if you don't create Payment by yourself and let
Mamona do it (e.g. by using mamona.views.process_order).
It must fill mandatory Payment fields: order and amount.
"""
