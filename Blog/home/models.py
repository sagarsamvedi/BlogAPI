from django.db import models
from django.contrib.auth.models import User
import uuid

'''
BaseModel is designed to be used as a base for other models in your Django application
'''
class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Blog(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog')
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    def __str__(self):
        return self.title