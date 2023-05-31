# モジュールのimport
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
# Create your models here.

def upload_avatar_path(instance, filename):
    ext = filename.split('.')[-1]

    # 保存先のファイルパスを生成
    # 生成されたファイルパスは 'avatars/{ユーザープロファイルのID}{ニックネーム}.{拡張子}'という形式になる
    return '/'.join(['avatars', str(instance.userProfile.id) + str(instance.nickName) + str(".") + str(ext)])




# UserManagerクラス
class UserManager(BaseUserManager):
    # create_userメソッドを定義(djangoの方で定義されてる)
    # 通常はユーザー名とパスワードだけど
    # 今回はemailとpasswordを引数に取り、新たなユーザーを作成してデータベースに保存する。
    def create_user(self, email, password=None):
        # もしemailが提供されていない場合、ValueErrorを発生させる
        if not email:
            raise ValueError('email is must')

        # normalize_emailメソッドを使用してemailを正規化（小文字化等）した後、新たなユーザーモデルのインスタンスを作成
        user = self.model(email=self.normalize_email(email))

        # set_passwordメソッドを使用してユーザーのパスワードを設定(このメソッドはパスワードをハッシュ化して保存する)
        user.set_password(password)

        # ユーザーインスタンスをデータベースに保存。
        user.save(using=self._db)

        # 作成したユーザーインスタンスを返す
        return user

    # create_superuserメソッドを定義
    # emailとpasswordを引数に取り、管理者権限を持つユーザーを作成する
    def create_superuser(self, email, password):

        # 既に定義されているcreate_userメソッドを利用して、ユーザーのインスタンスを作成
        user = self.create_user(email, password)

        # ユーザーのis_staffフラグをTrueに設定
        # is_staff：ユーザーが管理サイトにアクセスできるかどうかを制御するためのフラグ
        user.is_staff = True

        # ユーザーのis_superuserフラグをTrueに設定
        # is_superuser：ユーザーがすべてのオブジェクトと設定に対して全ての権限を持つかどうかを制御するためのフラグ
        user.is_superuser = True

        # フラグの変更を保存し、ユーザーインスタンスをデータベースに保存
        user.save(using=self._db)

        # 作成したユーザーインスタンスを返す
        return user


# ユーザーモデルの作成
class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=58, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # 上記で定義したUserManagerを使用してユーザーマネージャを作成
    # Userモデルにcreate_userメソッドやcreate_superuserメソッドが追加される
    objects = UserManager()

    # ユーザーモデルでユニークで必須のフィールドを指定。
    # 今回は'email'を指定して、ユーザーネームの代わりにメールアドレスを使用
    USERNAME_FIELD = 'email'

    # __str__メソッドを定義
    # このメソッドはオブジェクトを文字列として表現するためのもので、ここではユーザーのemailを返す
    # 管理画面等でユーザーオブジェクトを表示する際に使われる
    def __str__(self):
        return self.email


# Profileクラス
class Profile(models.Model):
    nickName = models.CharField(max_length=20)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='profile',
        on_delete=models.CASCADE
    )

    # プロファイルが作成された日時を保存するフィールド。DateTimeFieldは日時を保存するフィールド
    # auto_now_addパラメータ：Trueにすることで、レコードが作成されるときの日時を自動的にこのフィールドに保存する
    created_on = models.DateTimeField(auto_now_add=True)

    # 画像を保存するためのフィールド
    # blankパラメータ：Trueにすることでこのフィールドの入力が任意になります。
    # nullパラメータ：Trueにすることで、このフィールドがデータベースにおいてNULL値を取ることを許容します。
    # upload_toパラメータは画像ファイルのアップロード先を指定するためのもの(上記で記載)
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)



    def __str__(self):
        # __str__メソッドを定義します。このメソッドはオブジェクトを文字列として表現するためのもので、ここではユーザーのニックネームを返します。
        return self.nickName


# 投稿(記録)モデルの作成
# 評価を星で表示
SCORE_CHOICES = [
    (1, '★'),
    (2, '★★'),
    (3, '★★★'),
    (4, '★★★★'),
    (5, '★★★★★'),
]

class Post(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)  # 日付
    author = models.ForeignKey(  # 投稿者(多対1の関係で紐づく)
        settings.AUTH_USER_MODEL, related_name="posts",
        on_delete=models.CASCADE
    )
    restaurant_name = models.CharField(max_length=200)  # 店舗名
    location = models.CharField(max_length=200)  # 場所
    menu_item = models.CharField(max_length=200)  # メニュー名
    menu_item_photo = models.ImageField(upload_to='menu_photos/')  # メニュー画像
    menu_item_3d_model = models.FileField(upload_to='menu_3d_models/')  # メニュー3Dモデル
    price = models.IntegerField()  # 値段
    score = models.PositiveSmallIntegerField(verbose_name='レビュースコア', choices=SCORE_CHOICES, default='3')  #評価
    review_text = models.TextField()  # レビュー内容
    category = models.CharField(max_length=200)  # カテゴリー

