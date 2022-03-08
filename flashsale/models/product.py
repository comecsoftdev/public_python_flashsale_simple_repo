import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import FlashSaleUser
from flashsale.models.store import Store


def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return filename


class Product(models.Model):
    user = models.ForeignKey(FlashSaleUser, related_name='product', on_delete=models.CASCADE, primary_key=False)
    store = models.ForeignKey(Store, related_name='product', on_delete=models.CASCADE, primary_key=False)
    image = models.ImageField(verbose_name=_('Product Image'), upload_to=upload_to,)
    thumbnail = models.ImageField(verbose_name=_('Product Thumbnail'), upload_to=upload_to, null=True)
    name = models.CharField(verbose_name=_('Product Name'), max_length=50, null=False)
    comment = models.CharField(verbose_name=_('Comment About Product'), max_length=500, null=True)
    price = models.IntegerField(verbose_name=_('Product Price'), null=False,
                                validators=[MinValueValidator(100), MaxValueValidator(1000000)])
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    def __str__(self):
        return self.name
