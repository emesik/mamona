from django import forms
from django.forms.models import modelformset_factory
from order.models import Item

class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ('name', 'price')

ItemFormSet = modelformset_factory(Item, form=ItemForm, extra=5, max_num=5)
