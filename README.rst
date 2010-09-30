======
Mamona
======

Fully portable Django payments application
------------------------------------------

Mamona is a Django application for handling online payments. It can work with
any existing setup without a need of changing other applications' models.

Features:
    * accepts **any model** as *order* and creates *ForeignKey* relation to it,
    * requires **no interface** on *order* model,
    * can handle different payment gateways, just by enabling backends
      (at the moment, only PayPal and testing "dummy" backends are present),
    * can pass items list and customer data to the payment gateway,
    * offers signals to watch payment progress.

Any model as order, really?
---------------------------

Yes, thanks to great `AbstractMixin <http://gist.github.com/584106>`__ we can
attach *Payment* model to any other model, which represents an order, single item,
subscription plan, donation... whatever.

There are **no interface requirements** regarding the *order* model (it doesn't need
to be called *order*, either). The only thing you have to do, is to implement basic
set of signal listeners which extract essential data from your *order*.

These signals can reside in a standalone application, so there is no need to touch
the code of the app containing *order* model.

OK, tell me how to use it!
--------------------------

First of all, you have to install Mamona and add it to your ``settings.py`` file.

Second, you should enable the backends in ``settings.py`` and configure essential
parameters for gateways. The following example is for testing purposes, using
PayPal sandbox server and a test module called *dummy*.

::

    MAMONA_ACTIVE_BACKENDS = (
        'dummy',
        'paypal',
    )
    MAMONA_BACKENDS_SETTINGS = {
        'paypal': {
            'url': 'https://www.sandbox.paypal.com/cgi-bin/webscr',
            'email': 'me@my-email.com',
        },
    }

Third, knowing how your *order* model and it's environment is organized, you need to
implement listeners for two signals:

    * ``return_urls_query``, where you provide return URLs for successful and failed
      payments.
    * ``order_items_query``, where you fill a list of order items (or just return single
      item for simple orders).

Finally, build a *Payment* model connected together with your *order* model:

::

    from mamona.models import build_payment_model

    Payment = build_payment_model(MyOrderModel, unique=True, related_name='payments')

To check an example implementation, see ``test-project/cashier`` application. And also
refer to the source code of Mamona itself.
