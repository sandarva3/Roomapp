from django.db import models

class Text(models.Model):
    texts = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    Tunix_time = models.IntegerField(default=30)
    Taddress = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, default='27.34.64.148')
    Djip = models.TextField(max_length=12, null=True)

    def __str__(self):
        return self.texts

class Lanfiles(models.Model):
    file = models.FileField(upload_to='lanmedia', null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)
    Funix_time = models.IntegerField(default=60)
    Faddress = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, default='27.34.64.148')
    Djip = models.TextField(max_length=12, null=True)
    def __str__(self):
        return (self.file.name[9:])
    