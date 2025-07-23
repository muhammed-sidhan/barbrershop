from django.contrib import admin
from .models import User,BarberProfile,CustomerProfile,QueueEntry
# Register your models here.
admin.site.register(User)
admin.site.register(BarberProfile)
admin.site.register(CustomerProfile)
admin.site.register(QueueEntry)
