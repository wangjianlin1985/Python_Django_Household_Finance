from django.contrib import admin
from apps.Income.models import Income

# Register your models here.

admin.site.register(Income,admin.ModelAdmin)