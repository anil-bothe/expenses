from collections.abc import Iterable
from django.db import models
from app.model.base import Base
from app.model.users import User

class Expense(Base):
    payer = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    split_type = models.CharField(max_length=10, choices=[('EQUAL', 'Equal'), ('EXACT', 'Exact'), ('PERCENT', 'Percent')])
    participants = models.ManyToManyField(User, related_name="expenses")
    shares = models.JSONField(default=dict, blank=True) # For SHARE split_type
    
    # Optional
    name = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    images = models.ImageField(upload_to='expense_images', blank=True)


    def __str__(self):
        return str(self.payer.name)
        
    class Meta:
        db_table = 'expense'
        managed = True
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
