from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    TYPE_CHOICES = (("income", "Income"), ("expense", "Expense"))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    class Meta:
        unique_together = ("user", "name", "type")
        ordering = ["name"]
    def __str__(self):
        return f"{self.name} ({self.type})"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True)
    class Meta:
        ordering = ["-date", "-id"]


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField() # 1-12
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    class Meta:
        unique_together = ("user", "year", "month")
        ordering = ["-year", "-month"]