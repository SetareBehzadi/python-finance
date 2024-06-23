from django.contrib import admin

# Register your models here.
from finance.models import Payment, Gateway

admin.site.register(Payment)
admin.site.register(Gateway)