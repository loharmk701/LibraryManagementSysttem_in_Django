from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags, mark_safe
from django.utils.translation import gettext_lazy as _
from .models import Book, Student, Faculty, IssuedBook, BookIssuedHistory

# Try to import import-export for data import/export functionality
try:
    from import_export import resources
    from import_export.admin import ImportExportMixin
    import_export_installed = True
except ImportError:
    import_export_installed = False

# ------------------ Email Functions for Return & Warning Emails ------------------ #
def send_email_action(modeladmin, request, queryset):
    subject = "E.C / I.C.T Library"
    html_message = render_to_string("library/send_email.html")
    plain_message = strip_tags(html_message)

    for obj in queryset:
        if hasattr(obj, 'email') and obj.email:
            email = EmailMultiAlternatives(subject=subject, body=plain_message, from_email=None, to=[obj.email])
            email.attach_alternative(html_message, "text/html")
            email.send()

    messages.success(request, _("Emails sent successfully!"))

send_email_action.short_description = "Send Email: Confirm Return Book"

def send_warning_email(modeladmin, request, queryset):
    subject = "E.C / I.C.T Library"
    html_message = render_to_string("library/send_warning_email.html")
    plain_message = strip_tags(html_message)

    for obj in queryset:
        if hasattr(obj, 'email') and obj.email:
            email = EmailMultiAlternatives(subject=subject, body=plain_message, from_email=None, to=[obj.email])
            email.attach_alternative(html_message, "text/html")
            email.send()

    messages.success(request, _("Emails sent successfully!"))

send_warning_email.short_description = "Send Email: Book Overdue Warning"

# ------------------ Admin Resource Configuration (For Data Import/Export) ------------------ #
if import_export_installed:
    class BookResource(resources.ModelResource):
        class Meta:
            model = Book

    class StudentResource(resources.ModelResource):
        class Meta:
            model = Student

    class FacultyResource(resources.ModelResource):
        class Meta:
            model = Faculty

    class IssuedBookResource(resources.ModelResource):
        class Meta:
            model = IssuedBook

    class BookIssuedHistoryResource(resources.ModelResource):
        class Meta:
            model = BookIssuedHistory

# ------------------ Admin Class Configuration ------------------ #
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'isbn', 'publisher', 'quantity', 'display_qrcode')
    search_fields = ('title', 'author', 'isbn', 'publisher')
    ordering = ['title']
    
    def display_qrcode(self, obj):
        if obj.qrcode:
            return mark_safe(f'<img src="{obj.qrcode.url}" width="100" height="100" />')
        return "No QR Code"

    display_qrcode.short_description = "QR Code"

if import_export_installed:
    class BookAdmin(ImportExportMixin, BookAdmin):
        resource_class = BookResource

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'student_id', 'department','display_qrcode')
    search_fields = ('first_name', 'last_name', 'email', 'student_id', 'department')
    ordering = ['first_name']
    actions = [send_warning_email, send_email_action]

    def display_qrcode(self, obj):
        if obj.qrcode:
            return mark_safe(f'<img src="{obj.qrcode.url}" width="100" height="100" />')
        return "No QR Code"

    display_qrcode.short_description = "QR Code"

if import_export_installed:
    class StudentAdmin(ImportExportMixin, StudentAdmin):
        resource_class = StudentResource

class FacultyAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'faculty_id', 'department','display_qrcode')
    search_fields = ('first_name', 'last_name', 'email', 'faculty_id', 'department')
    ordering = ['first_name']
    actions = [send_warning_email, send_email_action]

    def display_qrcode(self, obj):
        if obj.qrcode:
            return mark_safe(f'<img src="{obj.qrcode.url}" width="100" height="100" />')
        return "No QR Code"

    display_qrcode.short_description = "QR Code"

if import_export_installed:
    class FacultyAdmin(ImportExportMixin, FacultyAdmin):
        resource_class = FacultyResource

class IssuedBookAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'issued_to_student', 'issued_to_faculty', 'issue_date', 'return_date', 'returned')
    search_fields = ('book__title', 'issued_to_student__first_name', 'issued_to_student__last_name', 'issued_to_faculty__first_name', 'issued_to_faculty__last_name')
    ordering = ['-issue_date']

if import_export_installed:
    class IssuedBookAdmin(ImportExportMixin, IssuedBookAdmin):
        resource_class = IssuedBookResource

class BookIssuedHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'issued_book_id', 'book', 'issued_to_name', 'issued_to_id', 'issue_date', 'return_date')
    search_fields = ('issued_book_id', 'book', 'issued_to_name', 'issued_to_id')
    ordering = ['-issue_date']

if import_export_installed:
    class BookIssuedHistoryAdmin(ImportExportMixin, BookIssuedHistoryAdmin):
        resource_class = BookIssuedHistoryResource

# ------------------ Register Admin Classes ------------------ #
admin.site.register(Book, BookAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(IssuedBook, IssuedBookAdmin)
admin.site.register(BookIssuedHistory, BookIssuedHistoryAdmin)
