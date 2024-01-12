from django.db import models
from app.model.base import Base
from app.model.users import User


class Balance(Base):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='balances_owed')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='balances_owed_to')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return str(self.user1.name)

    class Meta:
        db_table = 'balance'
        managed = True
        verbose_name = 'Balance'
        verbose_name_plural = 'Balances'
