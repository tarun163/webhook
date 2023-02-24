from django.db import models

# Create your models here.

class Messages(models.Model):
    msg_id = models.CharField(max_length=50,null=True,blank=True)
    status = models.CharField(max_length=15,default='Recieved')
    msg = models.TextField(default='')
    time_stamp = models.CharField(max_length=250,null=True,blank=True)

    display_name = models.CharField(max_length=100,null=True,blank=True)
    display_phone = models.CharField(max_length=15,null=True,blank=True)

    def __str__(self):
        return str(self.msg_id)
