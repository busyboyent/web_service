from django.db import models
from django.core.validators import URLValidator

class ParsedPage(models.Model):
    url = models.TextField(validators=[URLValidator()])
    h1_count = models.IntegerField(default=0)
    h2_count = models.IntegerField(default=0)
    h3_count = models.IntegerField(default=0)
    links = models.JSONField(default=list)  # Список ссылок
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
