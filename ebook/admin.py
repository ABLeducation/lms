from django.contrib import admin
from .models import *
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter

# Register your models here.
class ebooklessonadmin(admin.ModelAdmin):
    list_filter=(('book', RelatedDropdownFilter),)
    
class ebooksubjectadmin(admin.ModelAdmin):
    list_filter=(('grade', RelatedDropdownFilter),)
    
admin.site.register(Topic_name,ebooklessonadmin)
admin.site.register(Ebook,ebooksubjectadmin)