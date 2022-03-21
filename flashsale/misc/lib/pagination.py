from abc import ABC

from django.conf import settings

from django.core.paginator import Paginator as DjangoPaginator
from django.core.paginator import InvalidPage
from django.utils.translation import gettext_lazy as _

from rest_framework.pagination import BasePagination

from flashsale.misc.lib.exceptions import ArgumentWrongError


class CustomPagination(BasePagination, ABC):
    page_size = 10               # Number of objects to return in one page
    max_page_size = 200
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    page = None
    page_number = 1

    django_paginator_class = DjangoPaginator

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """

        self.page_size = request.data.get(self.page_size_query_param, self.page_size)
        if not self.page_size or int(self.page_size) > self.max_page_size:
            raise ArgumentWrongError(_('page_size not define or page_size is greater than max_page_size({})').format(self.max_page_size))

        paginator = self.django_paginator_class(queryset, self.page_size)
        self.page_number = request.data.get(self.page_query_param, 1)

        try:
            self.page = paginator.page(self.page_number)
        except InvalidPage as exc:
            raise ArgumentWrongError(_('{}Page .. Out of range').format(self.page_number))

        return list(self.page)

    def get_paginated_response(self, data):
        return {
            'total_count': int(self.page.paginator.count),
            'page_size': int(self.page_size),
            'page': int(self.page_number),
            'result': data
        }
