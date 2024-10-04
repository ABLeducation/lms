from django.contrib import admin
from .models import *
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter # type: ignore
from unfold.admin import ModelAdmin # type: ignore
from import_export.admin import ExportMixin # type: ignore
import openpyxl # type: ignore
from django.http import HttpResponse

# Register your models here.
class AnswerInLine(admin.TabularInline):
    model=Answer

class QuestionAdmin(ModelAdmin):
    inlines=[AnswerInLine]
    list_display=['text']
    list_filter=(
        ('quiz', RelatedDropdownFilter),
        )
    
class ResultAdmin(ExportMixin, ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'date_attempted', 'get_school', 'get_grade', 'get_section']
    
    # Correctly referencing the related fields from user_profile_student
    list_filter = (
        ('user__user_profile_student__school', DropdownFilter),  # Filtering by related School field
        ('user__user_profile_student__grade', DropdownFilter),  # Filtering by related Grade field
        ('user__user_profile_student__section', DropdownFilter),  # Filtering by related Section field
    )

    search_fields = ['user__username', 'quiz__name', 'user__user_profile_student__school', 'user__user_profile_student__grade']

    # Custom methods to display related fields in the list display
    def get_school(self, obj):
        return obj.user.user_profile_student.school
    get_school.short_description = 'School'

    def get_grade(self, obj):
        return obj.user.user_profile_student.grade
    get_grade.short_description = 'Grade'

    def get_section(self, obj):
        return obj.user.user_profile_student.section
    get_section.short_description = 'Section'
    
    
    # Admin action to export selected results to Excel
    actions = ['export_to_excel']

    def export_to_excel(self, request, queryset):
        # Create an in-memory workbook and worksheet
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = 'Results'

        # Write the header row
        headers = ['User', 'Quiz', 'Score', 'Date Attempted', 'School', 'Grade', 'Section']
        worksheet.append(headers)

        # Write the data rows
        for result in queryset:
            worksheet.append([
                result.user.username,
                result.quiz.name,
                result.score,
                result.date_attempted.strftime('%Y-%m-%d %H:%M:%S') if result.date_attempted else '',
                result.user.user_profile_student.school,
                result.user.user_profile_student.grade,
                result.user.user_profile_student.section
            ])

        # Prepare response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="results.xlsx"'

        # Save the workbook to the response
        workbook.save(response)
        return response

    export_to_excel.short_description = "Export selected results to Excel"

admin.site.register(Answer)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Quiz)
admin.site.register(Result, ResultAdmin)