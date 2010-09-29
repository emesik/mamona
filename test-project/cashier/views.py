from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404
from models import Order
from forms import OrderWithPaymentForm

def place_order(request):
	order = Order()
	if request.method == 'POST':
		form = OrderWithPaymentForm(data=request.POST)
		if form.is_valid():
			order.name = form.cleaned_data['name']
			order.total = form.cleaned_data['total']
			order.save()
			payment = order.checkout()
			next_step = form.proceed_to_gateway(payment)
			return HttpResponseRedirect(next_step)
	else:
		form = OrderWithPaymentForm()
	return direct_to_template(
		request,
		'cashier/place_order.html',
		{'form': form}
		)

def show_order(request, order_id):
	order = get_object_or_404(Order, id=order_id)
	return direct_to_template(
			request,
			'cashier/show_order.html',
			{'order': order}
			)
