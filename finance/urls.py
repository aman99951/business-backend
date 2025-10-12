from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, TransactionViewSet, BudgetViewSet, SummaryViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"transactions", TransactionViewSet, basename="transactions")
router.register(r"budgets", BudgetViewSet, basename="budgets")
router.register(r"summary", SummaryViewSet, basename="summary")

urlpatterns = [
    path("", include(router.urls)),
]