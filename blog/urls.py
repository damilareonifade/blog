from . import views
from django.urls import path
app_name= 'blog'

urlpatterns = [
    path('',views.index_page,name="index_page"),
    path('search',views.post_search, name='post_search'),
    path('<slug:post>',views.post_single, name='post_single'),
    path('category/<category>',views.CategoryListView.as_view(),name='catlist')
]
