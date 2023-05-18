from django.contrib import admin
from apps.IncomeType.models import IncomeType

# Register your models here.

admin.site.register(IncomeType,admin.ModelAdmin)