from django.urls import path
from . import views

app_name = 'shopsite'

urlpatterns = [
    path('', views.index , name='index'),  #一覧ページのビュー
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),   # 投稿詳細ページ
    path('create/', views.CreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.UpdateView.as_view(), name="update"),  # 投稿編集ページ
    path('<int:pk>/delete/', views.DeleteView.as_view(), name="delete"),  # 投稿削除ページ
    path('search/', views.search, name='search'),    # 検索
]