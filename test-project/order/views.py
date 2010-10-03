from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template

from models import UnawareOrder

def show_order(request, order_id):
	order = get_object_or_404(UnawareOrder, id=order_id)
	return direct_to_template(
			request,
			'order/show_order.html',
			{'order': order}
			)
