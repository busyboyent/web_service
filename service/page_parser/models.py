from django.db import models
from django.core.validators import URLValidator

class ParsedPage(models.Model):
    url = models.TextField(validators=[URLValidator()])
    h1 = models.IntegerField(default=0)
    h2 = models.IntegerField(default=0)
    h3 = models.IntegerField(default=0)
    a = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
