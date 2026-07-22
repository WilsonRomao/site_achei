from django.db import models

class Medicamento(models.Model):
    catmat = models.CharField(max_length=50, primary_key=True)
    medicamento = models.TextField()

    class Meta:
        db_table = "medicamento"

    def __str__(self):
        return self.medicamento