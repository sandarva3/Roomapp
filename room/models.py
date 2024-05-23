from django.db import models
import uuid

class Room(models.Model):
    text = models.TextField()
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    total_time = models.IntegerField(default=30)
    

    def __str__(self):
        return (f"Room code :{self.code}")
    

class Files(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    
