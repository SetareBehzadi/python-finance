import json
import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from finance.utils.zarinpal import zpal_request_handler


class Gateway(models.Model):
    """
    Save Gateways name and credentials to the db and use them to handle payment
    """

    FUNCTION_SAMAN = 'saman'
    FUNCTION_SHAPARAK = 'shaparak'
    FUNCTION_FINOTECH = 'finotech'
    FUNCTION_ZARRINPAL = 'zarinpal'
    FUNCTION_PARSIAN = 'parsian'
    GATEWAY_FUNCTIONS = (
        (FUNCTION_SAMAN, _("saman")),
        (FUNCTION_SHAPARAK, _("shaparak")),
        (FUNCTION_FINOTECH, _("finotech")),
        (FUNCTION_ZARRINPAL, _("zarinpal")),
        (FUNCTION_PARSIAN, _("parsian")),
    )

    title = models.CharField(max_length=100, verbose_name=_("gateway title"))
    gateway_request_url = models.CharField(max_length=150, verbose_name=_("request url"), null=True, blank=True)
    gateway_verify_url = models.CharField(max_length=150, verbose_name=_("verify url"), null=True, blank=True)
    gateway_code = models.CharField(max_length=12, verbose_name=_("gateway code"), choices=GATEWAY_FUNCTIONS)
    is_enable = models.BooleanField(verbose_name=_("is enable"), default=True)
    auth_data = models.TextField(verbose_name=_("auth_data"), null=True, blank=True)

    class Meta:
        verbose_name = _("Gateway")
        verbose_name_plural = _("Gateways")

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"[{self.__class__.__name__}({self.title})]"

    def get_request_handler(self):
        handlers = {
            self.FUNCTION_SAMAN: None,
            self.FUNCTION_SHAPARAK: None,
            self.FUNCTION_FINOTECH: None,
            self.FUNCTION_ZARRINPAL: zpal_request_handler,
            self.FUNCTION_PARSIAN: None,
        }
        return handlers[self.gateway_code]

    def credentials(self):
        return json.loads(self.auth_data)


class Payment(models.Model):
    invoice_number = models.UUIDField(verbose_name=_("invoice number"), unique=True, default=uuid.uuid4)
    amount = models.PositiveIntegerField(verbose_name=_("payment amount"), editable=True)
    gateway = models.ForeignKey(Gateway, related_name="payments", null=True, blank=True, verbose_name=_("gateway"),
                                on_delete=models.CASCADE)
    is_paid = models.BooleanField(verbose_name=_("is paid status"), default=False)
    payment_log = models.TextField(verbose_name=_("logs"), blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"), null=True, on_delete=models.SET_NULL)
    authority = models.CharField(max_length=64, verbose_name=_("authority"), blank=True)

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self):
        return self.invoice_number.hex

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._b_is_paid = self.is_paid

    @property
    def bank_page(self):
        handler = self.gateway.get_request_handler()
        if handler is not None:
            return handler(self.gateway, self)

    @property
    def title(self):
        return _("Instant payment")
