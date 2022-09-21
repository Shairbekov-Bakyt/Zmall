from rest_framework import pagination


class AdvertPagination(pagination.LimitOffsetPagination):
    default_limit = 25
    max_limit = 1000
    min_limit = 1
    min_offset = 1
    max_offset = 50
