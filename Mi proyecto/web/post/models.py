from django.db import models

class Post(models.Model):
    foto= models.ImageField(upload_to="fotos", null=False, blank=False)
    
    
    
