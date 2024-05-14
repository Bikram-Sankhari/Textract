from django.db import models
from accounts.models import User

# Create your models here.
class Customer(models.Model):
    surname = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        if self.name:
            return self.name
        else:
            return "None"
    
class CustomerDocument(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    attached_file1 = models.FileField(upload_to='uploads/', null=True, blank=True)
    attached_file2 = models.FileField(upload_to='uploads/', null=True, blank=True)
    extracted_json = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        if self.customer.name:
            return self.customer.name
        else:
            return "None"