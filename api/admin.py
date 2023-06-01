# Django adminとauth.adminから必要なモジュールをインポート
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# 多言語化をサポートするgettextをインポート
from django.utils.translation import gettext as _
# このアプリケーションのモデルをインポート
from . import models

# Register your models here.
# emailでカスタマイズした場合、adminへの登録の際にも設定を加える必要がある
class UserAdmin(BaseUserAdmin):
    # 管理画面のUserリストをid順に並べる
    ordering = ['id']
    # 管理画面のUserリストに表示するフィールド
    list_display = ['email']
    # Userの詳細画面でのフィールドのグループ化
    fieldsets = (
        # emailとpasswordのセクション
        (None, {'fields':('email', 'password')}),
        # 個人情報のセクション(フィールド未指定)
        (_('Personal Info'), {'fields': ()}),
        # 権限に関するセクション
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        # 最終ログイン日時に関するセクション
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    # Userを追加する画面でのフィールドの配置
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )

class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ['category']


# 開発者がオリジナルで作ったモデルはadminへの登録は簡単
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Profile)
admin.site.register(models.Post,PostAdmin)
admin.site.register(models.Restaurant)
admin.site.register(models.Category)