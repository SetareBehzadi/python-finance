from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View

from finance.forms import ChargeWalletForm
from finance.models import Payment, Gateway
from finance.utils.zarinpal import zpal_request_handler, zpal_payment_checker


class ChargeWalletView(View):
    template_name = 'charge_wallet.html'
    form_class = ChargeWalletForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            payment_link, authority = zpal_request_handler(
                settings.ZARINPAL['merchant_id'], form.cleaned_data['amount'],
                "wallet charge", 'rezam578@gmail.com', None, settings.ZARINPAL['gateway_callback_url']
            )
            if payment_link is not None:
                print(payment_link)
                print(authority)
                return redirect(payment_link)

        return render(request, self.template_name, {'form': form})


class VerifyView(View):
    template_name = 'callback.html'

    def get(self, request, *args, **kwargs):
        authority = request.GET.get('Authority')
        is_paid, ref_id = zpal_payment_checker(
            settings.ZARINPAL['merchant_id'], 10000, authority
        )
        return render(request, self.template_name, {'is_paid': is_paid, 'ref_id': ref_id})


class PaymentView(View):
    def get(self, request, invoice_number, *args, **kwargs):
        try:
            payment = Payment.objects.get(invoice_number=invoice_number)
        except Payment.DoesNotExist:
            raise Http404
        gateways = Gateway.objects.filter(is_enable=True)
        return render(request, 'finance/payment_detail.html', {'payment': payment, 'gateways': gateways})


class PaymentGatewayView(View):
    def get(self, request, invoice_number, gateway_code, *args, **kwargs):
        try:
            payment = Payment.objects.get(invoice_number=invoice_number)
        except Payment.DoesNotExist:
            raise Http404

        try:
            gateways = Gateway.objects.filter(gateway_code=True)
        except Gateway.DoesNotExist:
            raise Http404
        return render(request, 'finance/payment_detail.html', {'payment': payment, 'gateways': gateways})
