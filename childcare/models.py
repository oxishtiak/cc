from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff')
    mobile = models.CharField(max_length=25)
    address = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username
    
class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent')
    phone = models.CharField(max_length=25)
    address = models.CharField(max_length=255)
    
    def __str__(self):
        return self.user.username    

class Child(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(default=0)
    date_of_birth = models.DateField()
    image = models.ImageField(upload_to='child_images/')
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.name} ({self.unique_id})"


class Report(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="reports")
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="reports")
    children = models.ManyToManyField(Child, related_name="reports")
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Approved", "Approved")], default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Report ({self.status}) - {self.staff.user.username} - {self.booking.package.name}"


class Feedback(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="feedbacks")
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name="feedbacks")
    rating = models.PositiveIntegerField(default=0)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('booking', 'parent')

    def __str__(self):
        return f"Feedback ({self.rating}) - {self.parent.user.username} - {self.booking.package.name}"
