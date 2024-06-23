from django.contrib import admin
# Register your models here.
from django.contrib.admin import register

from package.models import Package, PackageAttribute


class PackageAttributeInline(admin.TabularInline):
    model = PackageAttribute


@register(Package)
class PackageModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    inlines = (PackageAttributeInline,)
