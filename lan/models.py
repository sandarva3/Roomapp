from django.db import models

class Text(models.Model):
    texts = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.texts