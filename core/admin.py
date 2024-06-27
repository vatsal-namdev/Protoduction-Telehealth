from django.contrib import admin
from .models import post, comment, query, doctor, ConsultationRequest, Plan, Subscription, Room, Message

# Register your models here.
admin.site.register(post)
admin.site.register(comment)
admin.site.register(query)
admin.site.register(doctor)
admin.site.register(ConsultationRequest)
admin.site.register(Plan)
admin.site.register(Subscription)
admin.site.register(Room)
admin.site.register(Message)