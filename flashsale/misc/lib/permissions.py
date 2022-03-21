from django.utils.translation import gettext_lazy as _

from rest_framework import permissions

from accounts.models import USER_TYPE_OWNER

from flashsale.misc.lib.exceptions import NoPermissionToAccess, ArgumentWrongError
from flashsale.models.product import Product
from flashsale.models.review import Review
from flashsale.models.store import Store


# check if user is USER_TYPE_OWNER
class IsUserTypeOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.type == USER_TYPE_OWNER:
            return True
        else:
            raise NoPermissionToAccess(_('User Type is not Owner'))


# check if user is owner of this Store
class IsStoreOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Store) and request.user == obj.user:
            return True
        else:
            raise NoPermissionToAccess(_('You are not owner of this store'))


# check if user is owner of product
class IsProductOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.store.id != int(request.data['store']):
            raise ArgumentWrongError(_('The product is not included in the store'))

        if isinstance(obj, Product) and request.user == obj.user and request.user == obj.store.user:
            return True
        else:
            raise NoPermissionToAccess(_('You are not owner of this product'))


# check if user is owner of review
class IsReviewOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Review) and request.user == obj.user:
            return True
        else:
            raise NoPermissionToAccess(_('You are NOT owner of this review'))
