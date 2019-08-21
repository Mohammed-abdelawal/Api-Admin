from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from myapp.views import CategoryViewSet, ArticleList, ArticleDetail, UserViewSet, is_auth


router = DefaultRouter()
router.register('category', CategoryViewSet)
router.register('user', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(router.urls)),
    path('api/article/',ArticleList.as_view()),
    path('api/article/<int:pk>/',ArticleDetail.as_view()),
    path('is_auth/',is_auth),
]


""" show your media files """ 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)


urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]