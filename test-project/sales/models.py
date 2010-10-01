from django.db import models
from order.models import UnawareOrder
from mamona.models import build_payment_model

# We build the final Payment model here, in external app,
# without touching the code containing UnawareObject.
build_payment_model(UnawareOrder, unique=False, related_name='payments')
import listeners
