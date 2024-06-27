from django.db import models
from datetime import datetime
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse
from django.utils import timezone


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
    
class doctor(models.Model):
    name = models.CharField(max_length=250)
    experience = models.TextField(max_length=600)
    detail = models.TextField(max_length=2000)
    post_img = models.ImageField(upload_to='dpost_images', null=True, blank=True)
    specialty = models.CharField(max_length=100, default=None)
    slug = AutoSlugField(populate_from='name', unique=True,null=True,default=None)
    
    def __str__(self):
        return '%s' % (self.name)
    

class ConsultationRequest(models.Model):
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20, blank=True)
    specialty = models.CharField(max_length=100)
    reason_for_consultation = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.specialty} Consultation"

    class Meta:
        ordering = ['-submitted_at']  # Order by most recent requests first

class Plan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField()  # Store features as a comma-separated list or JSON
    duration = models.IntegerField(help_text="Subscription duration in days (e.g., 30 for monthly)")

    def __str__(self):
        return self.name

    def calculate_end_date(self, start_date=None):
        if not start_date:
            start_date = timezone.now()
            return start_date + timezone.timedelta(days=self.duration)

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} Subscription"

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.plan.calculate_end_date(self.start_date)
            super().save(*args, **kwargs)

    def cancel(self):
        self.is_active = False
        self.save()

    def update_subscription_status(self):
        if self.end_date and self.end_date <= timezone.now():
            self.is_active = False
            self.save()


class Room(models.Model):
    name = models.CharField(max_length=1000)

class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=10000)
    room = models.CharField(max_length=10000)



