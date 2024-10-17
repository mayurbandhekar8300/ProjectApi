from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FirmAdminMOdel(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.SET_NULL)
    email = models.CharField(max_length=200,null=True,unique=True)
    name = models.CharField(max_length=200,null=True)
    created_at = models.DateField(auto_now=True)
    timestamp = models.DateTimeField(auto_now=True)
    
    
    
class InventroyItemModel(models.Model):
    itemName = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField()
    quantity = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=0)#0=not deleted #1=deleted
    created_at = models.DateField(auto_now=True)
    timestamp = models.DateTimeField(auto_now=True)
    firmAdmin = models.ForeignKey(FirmAdminMOdel,null=True,on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.itemName
    