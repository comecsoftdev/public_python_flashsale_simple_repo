from django.contrib import admin
from django.contrib.auth.models import Group

from social_django.admin import Association, Nonce, UserSocialAuth

from flashsale.admin import basic_data

# remove Django's Group from django Admin
admin.site.unregister(Group)

# Remove Python Social Auth from django admin
admin.site.unregister(Association)
admin.site.unregister(Nonce)
admin.site.unregister(UserSocialAuth)
