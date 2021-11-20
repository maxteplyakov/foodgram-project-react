from rest_framework.pagination import PageNumberPagination


class SubscriptionsPagination(PageNumberPagination):
    page_size_query_param = 'limit'

