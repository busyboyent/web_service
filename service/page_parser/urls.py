from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ParsedPageViewSet

router = DefaultRouter()
router.register(r'page', ParsedPageViewSet, basename='page')

urlpatterns = [
    path('page/create/', ParsedPageViewSet.as_view({'post': 'create_page'}), name='create-page'),
    path('page/<int:pk>/', ParsedPageViewSet.as_view({'get': 'get_page'}), name='get-page'),
    path('page/list/', ParsedPageViewSet.as_view({'get': 'list_pages'}), name='list-pages'),
] + router.urls