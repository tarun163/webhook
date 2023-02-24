from django.contrib import admin
from . models import *


class MessageAdmin(admin.ModelAdmin):
    list_display = ('display_name','msg','status','msg_id')
# Register your models here.
admin.site.register(Messages,MessageAdmin)