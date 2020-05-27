from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import CompanyViewSet, ProductViewSet, OrderViewSet, RemoveNoOrderBuyersView


router = SimpleRouter()

router.register('companies', CompanyViewSet, basename='companies')
router.register('products', ProductViewSet, basename='products')


urlpatterns = [
    path('orders/', OrderViewSet.as_view({'get': 'list', 'post': 'create'}), name='orders'),
    path('remove_lazy_buyers/', RemoveNoOrderBuyersView.as_view(), name='remove_lazy_buyers')
]

urlpatterns += router.urls