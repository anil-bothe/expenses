from django.db import models


class Roles(models.Model):
    name = models.CharField(max_length=18, null=True, blank=True, unique=True)

    class Meta:
        db_table = "roles"

    def __str__(self):
        return str(self.pk)
