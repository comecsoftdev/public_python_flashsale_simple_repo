from django.db import models
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver

from mptt.models import MPTTModel, TreeForeignKey


# MPTTModel is too slow for creating, updating.
# Category use MPTTModel because these don't update frequently
class Category(MPTTModel):
    name = models.CharField(verbose_name=_('Category Name'), max_length=30, unique=True)
    abbr = models.CharField(verbose_name=_('Category Name abbreviation'), max_length=12, unique=True)
    items = models.CharField(verbose_name=_('Category items example'), max_length=200)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


@receiver(models.signals.post_save, sender=Category)
def change_category_update_on_save(sender, instance, **kwargs):
    from flashsale.misc.lib.cache import delete_category_cache
    delete_category_cache()


@receiver(models.signals.post_delete, sender=Category)
def change_category_delete_on_save(sender, instance, **kwargs):
    from flashsale.misc.lib.cache import delete_category_cache
    delete_category_cache()
