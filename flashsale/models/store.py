from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from accounts.models import FlashSaleUser

from flashsale.models.basic_data import Category


class Store(models.Model):
    user = models.ForeignKey(FlashSaleUser, related_name='store', on_delete=models.CASCADE, primary_key=False)
    category = models.ForeignKey(Category, related_name='store', on_delete=models.CASCADE, primary_key=False)
    name = models.CharField(verbose_name=_('Store Name'), max_length=255)
    phone = models.CharField(verbose_name=_('Store Phone'), max_length=16, validators=[RegexValidator(regex='^\+\d{9,15}$', )])
    # Each .000001 difference in coordinate decimal degree is approximately 10 cm in length
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=False)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=False)
    address = models.CharField(verbose_name=_('Address'), max_length=255, null=False)  # store address
    address_detail = models.CharField(verbose_name=_('Address Detail'), null=True, max_length=255)  # address detail
    created = models.DateTimeField(_('Created'), auto_now_add=True)             # created time

    def __str__(self):
        return '{}({})'.format(self.name, self.user.__str__())
