from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('authen/', include('djoser.urls.jwt')),
]

# 静的メディアファイルを扱うためのURLパターンを追加
# MEDIA_URLとMEDIA_ROOTはsettings.pyで定義
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)