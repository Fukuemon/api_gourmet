# Djangoの認証システムからユーザーモデルを取得する関数をインポート
from django.contrib.auth import get_user_model
# Django Rest Frameworkからシリアライザーズをインポート
from rest_framework import serializers
from .models import Profile, Post, Restaurant, Category

# UserSerializer
class UserSerializer(serializers.ModelSerializer):
    # Metaクラスは、シリアライザーの動作を制御
    class Meta:
        # このシリアライザーが扱うモデルを指定。(ここではDjangoのUserモデルが使われる)
        model = get_user_model()
        # シリアライザーで取り扱いたいパラメーターの一覧を記入(この場合、ユーザーID、メールアドレス、パスワードが公開される)
        fields = ('id', 'email', 'password')
        # extra_kwargs：特定のフィールドに追加のオプションを指定するために使用される
        # 'write_only': True：パスワードを書き込み専用にする
        extra_kwargs = {'password': {'write_only': True}}

    # createメソッド：新しいユーザーインスタンスを作成
    # validated_data：バリデーションが成功したデータを含む辞書。
    def create(self, validated_data):
        # DjangoのUserモデルのcreate_userメソッドを使用して新しいユーザーを作成
        user = get_user_model().objects.create_user(**validated_data)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    # created_onフィールドをDateTimeFieldとして定義（"%Y-%m-%d"）でフォーマットしてシリアライズ)
    # read_only=True：このフィールドが読み取り専用
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    # Metaクラスはシリアライザーの動作を制御します。
    class Meta:
        # このシリアライザーが扱うモデル：Profileモデル
        model = Profile
        # ProfileモデルのどのフィールドをAPIで公開するかを定義(ID、ニックネーム、ユーザープロフィール、作成日時、画像が公開)
        fields = ('id', 'nickName', 'userProfile', 'created_on', 'img')
        # userProfileフィールドが読み取り専用（'read_only': True）であることを指定
        # Django側で自動でユーザの割り当てを行うようにする
        extra_kwargs = {'userProfile': {'read_only': True}}

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'location')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class PostSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%%m-%d", read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'author', 'restaurant', 'category', 'menu_item', 'score', 'price', 'menu_item_photo',
                  'menu_item_model', 'review_text')
        extra_kwargs = {'author': {'read_only': True}}