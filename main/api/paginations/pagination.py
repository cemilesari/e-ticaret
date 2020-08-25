from rest_framework.pagination import PageNumberPagination
class ProductPagination(PageNumberPagination):
    page_size = 5
class TemplatePagination(PageNumberPagination):
    page_size = 5
class LocationPagination(PageNumberPagination):
    page_size = 5
class BranchPagination(PageNumberPagination):
    page_size = 5
class CompanyPagination(PageNumberPagination):
    page_size = 5
class CategoryPagination(PageNumberPagination):
    page_size = 15 
class UserPagination(PageNumberPagination):
    page_size = 5
class CommentPagination(PageNumberPagination):
    page_size = 5
