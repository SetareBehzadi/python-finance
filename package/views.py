# Create your views here.
from django.shortcuts import render
from django.views import View

from package.models import Package


class PricingView(View):
    template_name = "package/pricing.html"
    model_class = Package

    def get_context_data(self):
        packages = self.model_class.objects.filter(is_enable=True)
        return dict(packages=packages)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
