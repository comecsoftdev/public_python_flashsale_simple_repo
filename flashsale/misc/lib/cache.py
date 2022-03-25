import logging

from collections import defaultdict

from django.core.cache import cache

from flashsale.serializer.basic_data import CategoryDetailSerializer

category_cache_key = 'category_cache'

logger = logging.getLogger(__name__)


def get_category_cache():
    try:
        category_data = cache.get(category_cache_key, None)
    except Exception as e:
        category_data = None
        logger.debug('Cache server Error {}'.format(e.__str__()))

    if category_data is None:
        from flashsale.models.basic_data import Category
        categories = Category.objects.all().select_related('parent').order_by('id')

        children_dict = defaultdict(list)
        root_node_dict = []
        for category in categories:
            if category.parent is not None:
                children_dict[category.parent.id].append(category)
            else:
                root_node_dict.append(category)

        category_data = CategoryDetailSerializer(root_node_dict, many=True, context={"children": children_dict}).data

        set_category_cache(category_data)

    return category_data


def set_category_cache(category):
    try:
        cache.set(category_cache_key, category, None)
    except Exception as e:
        logger.debug('Cache server Error {}'.format(e.__str__()))


def delete_category_cache():
    try:
        cache.delete(category_cache_key)
    except Exception as e:
        logger.debug('Cache server Error {}'.format(e.__str__()))