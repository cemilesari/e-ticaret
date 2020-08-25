from .home      import global_manage,home_view
from .product   import ProductListView,ProductCreateView,ProductUpdateView,ProductDetailView,ProductDeleteView
from .addresse  import AddresseView, AddresseDetail, NewAddresse,DeleteAddresseView, UpdateAddresseView
from .company   import CompanyDetail,NewCompany,UpdateCompanyView,DeleteCompanyView,CompanyView
from .category  import CategoryListView,NewCategoryView, DetailCategory
from .branches  import BranchesDetail,BranchesView,NewBranch,UpdateBranch,DeleteBranch 
from .templates import TemplatesList,TemplatesUpdate,TemplatesCreate,TemplatesDetail,TemplatesDelete
from .profile   import ProfileView
from .change_password import change_password
from .documentation   import DocumentationView