from django.db import models
from datetime import datetime
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class post(models.Model):
    title = models.CharField(max_length=100)
    user = models.CharField(max_length=70, default=None)
    post_img = models.ImageField(upload_to='post_images', null=True, blank=True)
    slug = AutoSlugField(populate_from='title', unique=True,null=True,default=None)
    body = RichTextField(blank=True,null=True,max_length=100000)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:post", kwargs={
            'slug':self.slug
        })
    

class query(models.Model):
    name = models.CharField(max_length=250,blank=True)
    body = models.TextField(max_length=100000)
    created = models.DateTimeField(default=datetime.now, blank=True)
    likes = models.ManyToManyField(User, related_name='post_query')

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('pcomment', args=(str(self.id)))

class comment(models.Model):
    # query = models.ForeignKey(query,related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    body = models.TextField(max_length=1000)
    date_added = models.DateTimeField(default=datetime.now)
    user = models.CharField(max_length=10000,blank=True)
    queryn = models.CharField(max_length=10000,blank=True)

    def __str__(self):
        return '%s-%s' % (self.queryn,self.name)
