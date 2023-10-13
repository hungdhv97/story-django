from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10  # Default to 10
    page_size_query_param = 'limit'  # Allow client to override, using `?limit=xxx`.
    max_page_size = 100  # Maximum limit allowed when using `?limit=xxx`.

    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'total_records': self.page.paginator.count,
                'total_pages': self.page.paginator.num_pages,
                'current_page': self.page.number,
                'next_page': self.page.next_page_number() if self.page.has_next() else None,
                'prev_page': self.page.previous_page_number() if self.page.has_previous() else None,
            },
            'results': data
        })
