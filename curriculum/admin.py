from django.contrib import admin
from .models import *
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter # type: ignore
from unfold.admin import ModelAdmin

# Register your models here.
class standardadmin(ModelAdmin):
    list_display=['name',]
    
def make_subject_displayable(modeladmin, request, queryset):
    queryset.update(display_on_frontend=True)

def make_subject_not_displayable(modeladmin, request, queryset):
    queryset.update(display_on_frontend=False)

make_subject_displayable.short_description = "Mark selected subjects as displayable"
make_subject_not_displayable.short_description = "Mark selected subjects as not displayable"

class subjectadmin(ModelAdmin):
    list_display=['name','standard','display_on_frontend']
    search_fields=('name',)
    list_filter=(('name', DropdownFilter),
        ('standard', RelatedDropdownFilter))
        
    actions = [make_subject_displayable, make_subject_not_displayable]

def make_displayable(modeladmin, request, queryset):
    queryset.update(display_on_frontend=True)

def make_not_displayable(modeladmin, request, queryset):
    queryset.update(display_on_frontend=False)

make_displayable.short_description = "Mark selected lessons as displayable"
make_not_displayable.short_description = "Mark selected lessons as not displayable"

class lessonadmin(ModelAdmin):
    list_display=['name','subject','Standard','display_on_frontend']
    # list_filter=['Standard','subject',]
    list_filter=(('name', DropdownFilter),
        ('Standard', RelatedDropdownFilter),
        ('subject', RelatedDropdownFilter)
        )
    search_fields=('name',)
    actions = [make_displayable, make_not_displayable]
    
class mechanzolessonadmin(ModelAdmin):
    list_display=['model_id','model_name']
    # list_filter=['Standard','subject',]
    list_filter=(('kit', RelatedDropdownFilter),
        )
    search_fields=('model_name',)

admin.site.register(Standard,standardadmin)
admin.site.register(Subject,subjectadmin)
admin.site.register(Lesson,lessonadmin)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(AISubject)
admin.site.register(AILesson)
admin.site.register(CodingSubject)
admin.site.register(CodingLesson)
admin.site.register(StudentResult)
admin.site.register(Mechanzo_kit_name)
admin.site.register(Mechanzo_model_name,mechanzolessonadmin)
admin.site.register(Topicwise_Marks)

def make_subject_displayable(modeladmin, request, queryset):
    queryset.update(display_on_frontend=True)

def make_subject_not_displayable(modeladmin, request, queryset):
    queryset.update(display_on_frontend=False)

make_subject_displayable.short_description = "Mark selected subjects as displayable"
make_subject_not_displayable.short_description = "Mark selected subjects as not displayable"

class teachersubjectadmin(ModelAdmin):
    list_display=['name','display_on_frontend']
    search_fields=('name',)
        
    actions = [make_subject_displayable, make_subject_not_displayable]
    
def make_displayable(modeladmin, request, queryset):
    queryset.update(display_on_frontend=True)

def make_not_displayable(modeladmin, request, queryset):
    queryset.update(display_on_frontend=False)

make_displayable.short_description = "Mark selected lessons as displayable"
make_not_displayable.short_description = "Mark selected lessons as not displayable"

class teacherlessonadmin(ModelAdmin):
    list_display=['name','subject','display_on_frontend']
    # list_filter=['Standard','subject',]
    list_filter=(('name', DropdownFilter),
                ('subject', RelatedDropdownFilter))
    search_fields=('name',)
    actions = [make_displayable, make_not_displayable]
admin.site.register(TeacherSubject,teachersubjectadmin)
admin.site.register(TeacherLesson,teacherlessonadmin)