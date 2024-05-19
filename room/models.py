from django.db import models
import uuid

class Room(models.Model):
    text = models.TextField()
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return (f"Room code :{self.code}")
    
