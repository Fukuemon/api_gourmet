from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'user'
# REST frameworkのDefaultRouterのインスタンスを作成
router = DefaultRouter()
# 'profile'パスとProfileViewSetをルーターに登録、これによりModelViewSet(CRUD関連)のエンドポイントが自動生成される
router.register('profile', views.ProfileViewSet)
# 他も同様に登録する
router.register('post', views.PostViewSet)
router.register('restaurant', views.RestaurantViewSet)
router.register('category', views.CategoryViewSet)

# DjangoのURLパターンを定義するurlpatternsリスト
# generics(汎用ビュー)で作ったViewのurlを設定する
urlpatterns = [
    # '/register/'パスへのリクエストをCreateUserViewビューにマッピングし、このパスを'register'という名前で参照できるようにする
    path('register/', views.CreateUserView.as_view(), name='register'),
    # '/myprofile/'パスへのリクエストをMyProfileListViewビューにマッピングし、このパスを'myprofile'という名前で参照できるようにする
    path('myprofile/', views.MyProfileListView.as_view(), name='myprofile'),
    # 投稿一覧
    path('post_list/', views.PostListView.as_view(), name='postlist'),
    # 投稿詳細
    path('post_detail/<str:pk>/', views.PostDetailView(), name="postdetail"),
    # ルーターに登録されたすべてのパスをルートURL（''）に含める、これにより上記で登録したパス（'profile', 'post', 'comment'）がURLとして使えるようになる
    path('',include(router.urls))

]