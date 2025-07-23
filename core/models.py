from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
class User (AbstractUser):
    ROLE_CHOICES=(('Barber','Barber'),
                  ('Customer','Customer'))
    role=models.CharField(max_length=10,choices=ROLE_CHOICES)

class BarberProfile (models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    shop_name=models.CharField(max_length=255)
    location=models.CharField( max_length=255)
    is_open=models.BooleanField(default=True)

    def __str__(self):
        return self.shop_name
    
class CustomerProfile (models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=20)
    location=models.CharField( max_length=255,blank=True,null=True)
    
    def __str__(self):
        return self.user.username

class QueueEntry(models.Model):
    barber=models.ForeignKey(BarberProfile,on_delete=models.CASCADE,related_name='queue_entries')
    customer=models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,related_name='queue_entries')
    joined_at=models.DateTimeField(default=timezone.now)
    is_active=models.BooleanField(default=True)
    class Meta:
        ordering=['joined_at']

    def __str__(self):
        return f"{self.customer.user.username } is in queue for {self.barber.shop_name}"
class BlockedCustomer(models.Model):
    barber=models.ForeignKey(BarberProfile,on_delete=models.CASCADE,related_name='blocked_customers')
    customer=models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,related_name='blocked_by_barbers')
    blocked_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.user.username} is blocked by {self.barber.shop_name}"
