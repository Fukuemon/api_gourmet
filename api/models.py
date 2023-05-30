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
