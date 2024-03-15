from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'limit'

    def paginate_queryset(self, queryset, request, view=None):
        return super(CustomPagination, self).paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response({
            'meta': {
                'pagination': {
                    'total_records': len(data),
                    'total_pages': self.page.paginator.num_pages,
                    'current_page': self.page.number,
                    'next_page': self.page.next_page_number() if self.page.has_next() else None,
                    'prev_page': self.page.previous_page_number() if self.page.has_previous() else None,
                }
            },
            'results': data
        })
