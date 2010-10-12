from django import forms
from django.forms.models import inlineformset_factory
from order.models import UnawareOrder, Item

class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ('name', 'price')

ItemFormSet = inlineformset_factory(UnawareOrder, Item, form=ItemForm, extra=5, max_num=5)
