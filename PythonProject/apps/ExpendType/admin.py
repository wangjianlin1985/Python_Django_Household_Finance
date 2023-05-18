from django.contrib import admin
from apps.ExpendType.models import ExpendType

# Register your models here.

admin.site.register(ExpendType,admin.ModelAdmin)