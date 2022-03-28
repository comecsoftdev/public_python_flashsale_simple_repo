from mptt.admin import MPTTModelAdmin

from django.contrib import admin

from flashsale.models.basic_data import Category


class CategoryAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 40
    list_display = ('id', 'name', 'abbr', 'items', )
    ordering = ('id',)

    # Can't delete category
    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return True


admin.site.register(Category, CategoryAdmin)
