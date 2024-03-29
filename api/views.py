from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from . import serializers
from .models import Profile, Post, Restaurant, Category
# Create your views here.

# CreateUserView:新規ユーザーを作成するためのAPIエンドポイント
class CreateUserView(generics.CreateAPIView):
    # UserSerializerを使用してユーザーデータをシリアライズ
    serializer_class = serializers.UserSerializer
    # このビューに対するパーミッションを設定
    # 誰でも（ログインしているユーザーでなくても）新規ユーザーを作成できるようにする
    permission_classes = (AllowAny,)

# ProfileViewSet；プロフィールデータに対するCRUD（Create, Read, Update, Delete）操作を提供するAPIエンドポイント
class ProfileViewSet(viewsets.ModelViewSet):
    # このビューセットが扱うデータのクエリセットを指定(Profileモデルのすべてのインスタンスを取得)
    queryset = Profile.objects.all()

    # ProfileSerializerを使用してプロフィールデータをシリアライズ
    serializer_class = serializers.ProfileSerializer

    # perform_createは新規オブジェクトを作成するときにオーバーライドすることができるメソッド
    # 新規プロフィールのuserProfileフィールドを現在認証されているユーザーに設定
    def perform_create(self, serializer):
        serializer.save(userProfile=self.request.user)

# MyProfileListView：プロフィールの一覧を取得するためのエンドポイント
class MyProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    def get_queryset(self):
        return self.queryset.filter(userProfile=self.request.user)

# RestaurantViewSet：店舗情報に対するCRUD（Create, Read, Update, Delete）操作を提供するAPIエンドポイント
class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer
    permission_classes = (AllowAny,)

# CategoryViewSet：カテゴリーに対するCRUD（Create, Read, Update, Delete）操作を提供するAPIエンドポイント
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (AllowAny,)

# PostViewSet：投稿に対するCRUD（Create, Read, Update, Delete）操作を提供するAPIエンドポイント
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# 投稿一覧取得(誰でもアクセス可能)
class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = (AllowAny,)

class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = (AllowAny,)

