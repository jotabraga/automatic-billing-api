from django.db import models


class FileUploaded(models.Model):

    STATUS = [
        ("success", "Sucesso"),
        ("fail", "Falha"),
    ]

    name = models.TextField(null=False, blank=False)
    status = models.CharField(max_length=30, null=False, blank=False, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
