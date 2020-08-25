# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import url
from django.urls import path, re_path, include
from .views import *
from main.api.views.reseller.product import *
from main.api.views.reseller.product_template import *
from main.api.views.reseller.locations import *
from main.api.views.reseller.branches import *
from main.api.views.reseller.categories import *
from main.api.views.reseller.companies import * 
from main.api.views.reseller.favorites import *
from main.api.views.reseller.comments import *
from main.api.views.reseller import *
from main.api.views.user import *
from rest_framework_simplejwt import views as jwt_views
from django.views.decorators.cache import cache_page

app_name = 'api'

urlpatterns = [
    path('auth/', include(arg=[
        path('token/',              view=jwt_views.TokenObtainPairView.as_view(),   name='token_obtain_pair'),
        path('token/refresh/',      view=jwt_views.TokenRefreshView.as_view(),      name='token_refresh'),
        path('token/verify/',       view=jwt_views.TokenVerifyView.as_view(),       name='token_verify'),
        path('',                    view=AuthRouteView.as_view(),                   name='auth_route_view',),
    ])),

    path('consumer/', include(arg=[
        path('', view=ConsumerRouteView.as_view(), name='consumer_route_view',),
    ])),

    path('user/', include(arg=[
        path('', view=UserRouteView.as_view(), name='user_route_view',),
        path('user-list/', view=UserListView.as_view(),  name='user_list_view'),
        path('user-detail/<int:pk>/', view=LocationDetailAPIView.as_view(), name='user-detail-view'),
        path('user/products/', view=LocationDetailForAPIView.as_view(), name='user-for-product'),

        
    ])),

    path('reseller/', include(arg=[
        path('',                            view=ResellerRouteView.as_view(),     name='reseller_route_view',),
        path('product/' , include(arg=[
            path('',                            view=ProductRouteView.as_view(),      name="product_route_view",),
            #product list cache **
            path('product-list/',               cache_page(60 * 1)(ProductListAPIView.as_view()),    name="product_list_view",),
            path('product-detail/<int:pk>',     view=ProductDetailAPIView.as_view(),  name='product_detail_view',),
            path('product-create/',             view=ProductCreateAPIView.as_view(),  name="product_create_view",),
            
        ])),
        path('template/' , include(arg=[
            path('',                                    view=TemplateRouteView.as_view(),              name="template_route_view",),
            path('product-template-list/',              view=ProductTemplateListAPIView.as_view(),     name="product_template_list",),
            path('product-template-create/',            view=ProductTemplateCreateAPIView.as_view(),   name="product_template_create",),
            path('product-template-detail/<int:pk>',    view=ProductTemplateDetailAPIView.as_view(),   name="product_template_detail",),

        ])),
        path('branch/' , include(arg=[
            path('',                             view=BranchRouteView.as_view(),    name="branch_route_view",),
            path('branch-list/',                 view=BranchListAPIView.as_view(),  name="branch_list_view",),
            path('branch-create/',               view=BranchCreateAPIView.as_view(),name="branch_create_view",),
            path('branch-detail/<int:pk>',       view=BranchDetailAPIView.as_view(),name="branch_detail_view",),
            
        ])),
        path('company/' , include(arg=[
            path('',                             view=CompanyRouteView.as_view(),    name="company_route_view",),
            path('company-list/',                view=CompanyListAPIView.as_view(),  name="company_list_view",),
            path('company-create/',              view=CompanyCreateAPIView.as_view(),name="company_create_view",),
            path('company-detail/<int:pk>',      view=CompanyDetailAPIView.as_view(),name="company_detail_view",),
            path('company-detail/<int:pk>/produts', view=CompanyDetailProductAPIView.as_view(),name="product_for_company",),
        ])),
       
        path('location/' , include(arg=[
            path('',                             view=LocationRouteView.as_view(),         name="location_route_view",),
            path('location-list/' ,               view=LocationListApiView.as_view(),      name="location-list-view",),
            path('location-detail/<int:pk>',     view=LocationDetailAPIView.as_view(),     name="location_detail_view",),
            path('location-detail/<int:pk>/products',     view=LocationDetailForProductAPI.as_view(),     name="product_for_location",),

            path('location-create/',             view=LocationCreateAPIView.as_view(),     name="location_create_view"),

        ])),
        path('category/' , include(arg=[
            path('',                             view=CategoryRouteView.as_view(),    name="category_route_view",),
            path('category-list/',               view=CategoryListAPIView.as_view(),  name="category_list_view",),
            path('category-detail/<int:pk>',     view=CategoryDetailAPIView.as_view(),name="category_detail_view",),
            path('category-create/',             view=CategoryCreateAPIView.as_view(),name="category_create_view",),
        
        ])),
        path('favorite/' , include(arg=[
            path('',                             view=FavoriteRouteView.as_view(),           name="favorite_route_view",),
            path('favourite-list/',              view=FavouriteListCreateAPIView.as_view(),  name="favorite_list_view",),
            path('update-delete/<int:pk>',       view=FavoriteAPIView.as_view(),             name="favorite_update_delete"),
            path('favorites-detail/<int:pk>',    view=FavoritesDetailAPIView.as_view(),       name="favorite_detail_view",),

        ])),
        path('comments/', include(arg=[
            path('',                             view=CommentsRouteView.as_view(),            name="product_comment_view"),
            path('product_comments_create/',     view=CommentCreateAPIView.as_view(),         name="product_comment_create"),
            path("product_comments_list/",       view=CommentListAPIView.as_view(),           name="product_comment_list"),
            path("product_comment_delete/",      view=CommentDeleteAPIView.as_view,           name="product_comment_delete"),
            path("product_comment_update/",      view=CommentUpdateAPIView.as_view,           name="product_comment_update"),
            
            
        ])),
    ])),
    path('', view=MainRouteView.as_view(), name='main_route_view',),
]