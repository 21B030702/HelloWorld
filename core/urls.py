from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, CategoryViewSet, SupplierViewSet, 
    ItemViewSet, AuctionViewSet, ReviewViewSet, PurchaseViewSet
)
from .views import regist, CustomAuthToken
from django.urls import re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'items', ItemViewSet)
router.register(r'auctions', AuctionViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'purchases', PurchaseViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Hello World!",
      default_version='v1',
      description='''Добро пожаловать в документацию Hello World! Здесь вы найдете полное руководство по всем доступным конечным точкам и их использованию.

        ## Аутентификация

        Большинство конечных точек требуют аутентификации. Мы используем токен-базированную аутентификацию. Чтобы получить токен, вам нужно зарегистрироваться и использовать конечную точку получения токена.

        ## Работа с моделями

        Вам доступны конечные точки для работы с пользователями, категориями, поставщиками, товарами и аукционами. Вы можете просматривать, создавать, редактировать и удалять записи с использованием соответствующих HTTP-методов.

        ## Отзывы и покупки

        Пользователи могут оставлять отзывы на товары и участвовать в покупках и аукционах. Вся информация о транзакциях и отзывах сохраняется и доступна через API.

        Для получения более детальной информации о каждой конечной точке перейдите на соответствующие страницы Swagger или ReDoc, доступные через интерфейс API.
        """, ''',
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@myapi.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', CustomAuthToken.as_view(), name='token-auth'),
    path('api/register/', regist, name='regist'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]