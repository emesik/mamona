from django.dispatch import Signal

payment_status_changed = Signal(providing_args=['old_status', 'new_status'])

order_items_query = Signal(providing_args=['items'])
customer_data_query = Signal(providing_args=['customer'])
return_urls_query = Signal(providing_args=['urls'])
order_to_payment_query = Signal(providing_args=['order', 'payment'])
