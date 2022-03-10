import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.dispatch import receiver
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


# remove old image files when product is updated
@receiver(models.signals.pre_save, sender=Product)
def pre_save_processing(sender, instance, **kwargs):
    # instance.pk == None means new image inserted
    if not instance.pk:
        return False

    try:
        # get old image of product
        old_image = Product.objects.get(pk=instance.pk).image
    except Product.DoesNotExist:
        return False

    # get new image of product
    new_image = instance.image

    # delete old image
    if new_image and old_image and not new_image.__eq__(old_image):
        old_image.delete(save=False)


@receiver(models.signals.post_delete, sender=Product)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
