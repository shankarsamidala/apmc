
# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import Faculty, StudentCall

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'full_name', 'department', 'phone', 'role', 'is_active', 'is_staff')
    list_filter = ('department', 'role', 'is_active', 'is_staff')
    search_fields = ('emp_id', 'full_name', 'phone', 'department')
    ordering = ('full_name',)
    readonly_fields = ('last_login', 'date_joined')

    fieldsets = (
        ('Personal Info', {
            'fields': ('emp_id', 'full_name', 'department', 'phone', 'role')
        }),
        ('Authentication', {
            'fields': ('username', 'email', 'password')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(role='staff')  # Restrict non-superusers from seeing admins
        return qs


class StudentCallAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'faculty', 'phone_1', 'call_1_status', 'formatted_call_date')
    list_filter = ('call_1_status',  'created_at')
    search_fields = ('student_name', 'phone_1', 'faculty__full_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    list_per_page = 25  # Pagination
    
    fieldsets = (
        ('Faculty Assignment', {
            'fields': ('faculty',)
        }),
        ('Student Details', {
            'fields': ('student_name', 'phone_1', 'phone_2', 'inter_group', 'inter_marks', 'exam_rank')
        }),
        ('Call Status', {
            'fields': ('call_1_status', 'call_2_status', 'call_3_status')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )

    def formatted_call_date(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    formatted_call_date.short_description = "Call Date"

    def colored_call_status(self, obj):
        status_color_map = {
            'pending': 'orange',
            'answered': 'green',
            'not_answered': 'red',
            'wrong_number': 'gray',
        }
        color = status_color_map.get(obj.call_1_status, 'black')
        return format_html(f'<span style="color: {color}; font-weight: bold;">{obj.call_1_status}</span>')

    colored_call_status.short_description = "Call 1 Status"

admin.site.register(StudentCall, StudentCallAdmin)
