# モジュールのimport
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
# Create your models here.

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
