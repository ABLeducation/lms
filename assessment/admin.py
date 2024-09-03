from django.contrib import admin
from .models import *
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter
from unfold.admin import ModelAdmin # type: ignore

# Register your models here.
class AnswerInLine(admin.TabularInline):
    model=Answer

class QuestionAdmin(ModelAdmin):
    inlines=[AnswerInLine]
    list_display=['text']
    list_filter=(
        ('quiz', RelatedDropdownFilter),
        )

admin.site.register(Answer)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Quiz)
admin.site.register(Result)