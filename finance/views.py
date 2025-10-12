from datetime import date
from calendar import monthrange
from django.db.models import Sum, Q
from rest_framework import viewsets, mixins, permissions, decorators, response, status
from .models import Category, Transaction, Budget
from .serializers import CategorySerializer, TransactionSerializer, BudgetSerializer
from .permissions import IsOwner

class OwnedQuerysetMixin:
    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)
        # Filtering for transactions
        if self.basename == "transactions":
            p = self.request.query_params
            if p.get("category"):
                qs = qs.filter(category_id=p["category"])
            if p.get("type") in ("income", "expense"):
                qs = qs.filter(category__type=p["type"])
            if p.get("min_amount"):
                qs = qs.filter(amount__gte=p["min_amount"])
            if p.get("max_amount"):
                qs = qs.filter(amount__lte=p["max_amount"])
            if p.get("start_date"):
                qs = qs.filter(date__gte=p["start_date"])
            if p.get("end_date"):
                qs = qs.filter(date__lte=p["end_date"])
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewSet(OwnedQuerysetMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

class TransactionViewSet(OwnedQuerysetMixin, viewsets.ModelViewSet):
    queryset = Transaction.objects.select_related("category").all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

class BudgetViewSet(OwnedQuerysetMixin, viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def create(self, request, *args, **kwargs):
        # Check if budget already exists for this user, year, and month
        year = request.data.get('year')
        month = request.data.get('month')
        
        if year and month:
            existing_budget = Budget.objects.filter(
                user=request.user,
                year=year,
                month=month
            ).first()
            
            if existing_budget:
                # Update existing budget instead of creating a new one
                serializer = self.get_serializer(existing_budget, data=request.data, partial=False)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return response.Response(serializer.data, status=status.HTTP_200_OK)
        
        # If no existing budget, proceed with normal creation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @decorators.action(detail=False, methods=["get"], url_path="current")
    def current(self, request):
        today = date.today()
        b = Budget.objects.filter(user=request.user, year=today.year, month=today.month).first()
        total_expense = Transaction.objects.filter(
            user=request.user, 
            category__type="expense", 
            date__year=today.year, 
            date__month=today.month
        ).aggregate(sum=Sum("amount"))["sum"] or 0
        return response.Response({
            "budget": BudgetSerializer(b).data if b else None,
            "actual_expense": total_expense,
        })

class SummaryViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        totals = Transaction.objects.filter(user=user).values("category__type").annotate(total=Sum("amount"))
        total_income = sum(t["total"] for t in totals if t["category__type"] == "income") or 0
        total_expense = sum(t["total"] for t in totals if t["category__type"] == "expense") or 0
        balance = total_income - total_expense
        # per-category breakdown for charts
        categories = (
            Transaction.objects.filter(user=user)
            .values("category__name", "category__type")
            .annotate(total=Sum("amount"))
            .order_by("category__type", "category__name")
        )
        return response.Response({
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
            "by_category": list(categories),
        })