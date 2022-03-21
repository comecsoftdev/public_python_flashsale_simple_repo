from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import FlashSaleUser
from flashsale.models.store import Store

REVIEW_RATING_CHOICES = (
    (1, 'Poor'),
    (2, 'Average'),
    (3, 'Good'),
    (4, 'Very Good'),
    (5, 'Excellent')
)


# create review table to process review and rating Simultaneously
class Review(models.Model):
    # Reviewer( user' review or store_owner's reply)
    user = models.ForeignKey(FlashSaleUser, related_name='review', on_delete=models.CASCADE, primary_key=False)
    store = models.ForeignKey(Store, related_name='review', on_delete=models.CASCADE, primary_key=False)
    review = models.CharField(max_length=600)
    # null in case of store_owner's reply
    rating = models.IntegerField(choices=REVIEW_RATING_CHOICES, null=True)
    parent = models.OneToOneField('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    def __str__(self):
        return self.review[:40]

