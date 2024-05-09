from django.db import models


class FileUploaded(models.Model):

    STATUS = [
        ("success", "Sucesso"),
        ("fail", "Falha"),
    ]

    name = models.TextField(max_length=8, null=False, blank=False)

    status = models.CharField(max_length=30, null=False, blank=False, choices=STATUS)

    created_at = models.DateTimeField(auto_now_add=True)
