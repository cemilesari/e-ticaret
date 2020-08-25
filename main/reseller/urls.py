from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import url
from django.urls import path, re_path, include
from django.contrib.auth.decorators import login_required
from .views import *
from .views import DocumentationView
app_name = 'reseller'

urlpatterns = [
	path('manage/'        			 , global_manage  									    , name='global_manage'),
	#addresse
	path('address-list/'             ,  view=login_required(AddresseView.as_view())         , name="addresse_view"),
	path('address-create/'           ,  view=login_required(NewAddresse.as_view())          , name="addresse_create"),
	path('address-update/<int:pk>'   ,  view=login_required(UpdateAddresseView.as_view())   , name="addresse_update"),
	path('address-detail/<int:pk>'   ,  view=login_required(AddresseDetail.as_view())       , name="addresse_detail"),
	path('address-delete/'		     ,  view=login_required(DeleteAddresseView.as_view())   , name="addresse_delete"),

	#category transaction 
	path('category-list/'                ,  view=login_required(CategoryListView.as_view())  , name="category_view"),
	path('category-create/'              ,  view=login_required(NewCategoryView.as_view())   , name="category_create"),
	path('category-product-list/<int:pk>',  view=login_required(DetailCategory.as_view())    , name="category_detail"),
	
	#company transactions
	path('company-list/'             ,  view=login_required(CompanyView.as_view())          , name='company_list'),
	path('company-update/<int:pk>'   ,  view=login_required(UpdateCompanyView.as_view())    , name='update_company'),
	path('company-create/'   	     ,  view=login_required(NewCompany.as_view())    		, name='create_company'),
	path('company-detail/<int:pk>'   ,  view=login_required(CompanyDetail.as_view())        , name='detail_company'),
	path('company-delete/'           ,  view=login_required(DeleteCompanyView.as_view())    , name='delete_company'),
    
	#branch transactions
	path('branch-list/'              ,  view=login_required(BranchesView.as_view())         , name='branch_list'),
	path('branch-update/<int:pk>'    ,  view=login_required(UpdateBranch.as_view())         , name='update_branch'),
	path('branch-create/'   	     ,  view=login_required(NewBranch.as_view())    		, name='create_branch'),
	path('branch-detail/<int:pk>'    ,  view=login_required(BranchesDetail.as_view())       , name='detail_branch'),
	path('branch-delete/'            ,  view=login_required(DeleteBranch.as_view())         , name='delete_branch'),
  
	#product template transactions
	path('template-list/'            ,  view=login_required(TemplatesList.as_view())        , name='template_list'),
	path('template-update/<int:pk>'  ,  view=login_required(TemplatesUpdate.as_view())      , name='template_update'),
	path('template-create/'          ,  view=login_required(TemplatesCreate.as_view())      , name='template-create'),
	path('template-detail/<int:pk>'  ,  view=login_required(TemplatesDetail.as_view())      , name='template_detail'),
	path('template-delete/'          ,  view=login_required(TemplatesDelete.as_view())      , name='template_delete'),
	
	#product transactions
	path('product-list/'             ,  view=login_required(ProductListView.as_view())      , name='product_list'),
	path('product-update/<int:pk>'   ,  view=login_required(ProductUpdateView.as_view())    , name='update_product'),
	path('product-create/'   	     ,  view=login_required(ProductCreateView.as_view())    , name='create_product'),
	path('product-detail/<int:pk>'   ,  view=login_required(ProductDetailView.as_view())    , name='detail_product'),
	path('product-delete/'           ,  view=login_required(ProductDeleteView.as_view())    , name='delete_product'),
	
    path('documentation/'            ,  view=DocumentationView.as_view()                    , name="documentation_api_view"),

	#profile_view
	path(''                          ,  view=login_required(ProfileView.as_view())           , name="profile_view"),
	path('change-password/'          ,  view=change_password                                 , name="change_password")
]
