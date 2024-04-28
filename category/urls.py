
from django.urls import path
from .views import CategoryListCreateView, CategoryRetrieveUpdateDestroyView,SubCategoryListCreateView,SubCategoryRetrieveUpdateDestroyView
# from . import views 
urlpatterns = [
    # path('createCategory/', views.Createcategory, name='categorycreate'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),
    path('subcategories/', SubCategoryListCreateView.as_view(), name='subcategory-list'),
    path('subcategories/<int:pk>/', SubCategoryRetrieveUpdateDestroyView.as_view(), name='subcategory-detail'),
]