from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            "page": self.page.number,
            "total_pages": self.page.paginator.num_pages,
            'results': data
        })