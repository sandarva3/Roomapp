from django.db import models

class Text(models.Model):
    texts = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    Tunix_time = models.IntegerField(default=30)
    Taddress = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, default='27.34.64.148')

    def __str__(self):
        return self.texts
        

class Lanfiles(models.Model):
    file = models.FileField(upload_to="lanmedia", null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)
    Funix_time = models.IntegerField(default=60)
    Faddress = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, default='27.34.64.148')

    def __str__(self):
        return (self.file.name[9:])
        

class FilesHistory(models.Model):
    file_name = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)
    Faddress = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, default='27.34.64.148')
    def __str__(self):
        return self.file_name


'''   class IpObject(models.Model):
    IP  = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, default='27.34.64.148')
    texts = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='lanmedia', null=True)
    uploaded_at = models.DateTimeField(null=True)
    modified_at = models.DateTimeField(auto_now=True)


class Allthings(models.Model):
    Ip_object = models.ForeignKey()
    texts = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(null=True)
    uploaded_at = models.DateTimeField(null=True)
    modified_at = {
        models.DateTimeField, texts
    }
    deletion_time = {
        models.DateTimeField(), filename
    }   '''