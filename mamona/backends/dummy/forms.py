import datetime
from ...forms import ConfirmationForm
from . import models

class DummyConfirmationForm(ConfirmationForm):
	def __init__(self, *args, **kwargs):
		super(DummyConfirmationForm, self).__init__(*args, **kwargs)
		# An example how payment backend could create additional models related to Payment:
		txn = models.DummyTxn.objects.create(
				payment=self.payment,
				comment="Dummy transaction created on %s" % datetime.datetime.now()
				)
