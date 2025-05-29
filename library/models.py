from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image

# Book model
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    publisher = models.CharField(max_length=255)
    publication_date = models.DateField()
    quantity = models.IntegerField()
    qr_code = models.ImageField(upload_to='qr_codes/books/', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        data = f"Book Title: {self.title}\n ISBN: {self.isbn}\n Author: {self.author}"
        qr = qrcode.make(data)

        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        fname = f'book_qr_{self.isbn}.png'
        self.qr_code.save(fname, File(buffer), save=False)

        super().save(*args, **kwargs)

# Student model
class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    student_id = models.CharField(max_length=12, unique=True)
    department = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to='qr_codes/students/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save to get ID

        data = f"First Name: {self.first_name}\n Last Name: {self.last_name}\n Student Id: {self.student_id}\n Department: {self.department}"
        qr = qrcode.make(data)

        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        fname = f'student_qr_{self.student_id}.png'
        self.qr_code.save(fname, File(buffer), save=False)

        super().save(*args, **kwargs)  # Save again with QR

# Faculty model
class Faculty(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    faculty_id = models.CharField(max_length=10, unique=True)
    department = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to='qr_codes/faculty/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.faculty_id})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        data = f"First Name: {self.first_name}\n Last Name: {self.last_name}\n Faculty Id: {self.faculty_id}\n Department: {self.department}"
        qr = qrcode.make(data)

        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        fname = f'faculty_qr_{self.faculty_id}.png'
        self.qr_code.save(fname, File(buffer), save=False)

        super().save(*args, **kwargs)

# IssuedBook model
class IssuedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="issued_books")
    issued_to_student = models.ForeignKey(Student, null=True, blank=True, on_delete=models.SET_NULL, related_name="issued_books")
    issued_to_faculty = models.ForeignKey(Faculty, null=True, blank=True, on_delete=models.SET_NULL, related_name="issued_books")
    issue_date = models.DateField()
    return_date = models.DateField()
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"Issued: {self.book.title} to {'Student' if self.issued_to_student else 'Faculty'}"

# BookIssuedHistory model
class BookIssuedHistory(models.Model):
    issued_book_id = models.CharField(max_length=90, null=True, blank=True)  # Stores IssuedBook ID as a reference
    book = models.CharField(max_length=255, null=True, blank=True)  # Stores book title for historical purposes
    issued_to_student_faculty = models.CharField(max_length=10, null=True, blank=True)  # "Student" or "Faculty"
    issued_to_name = models.CharField(max_length=255, null=True, blank=True)  # Stores the name of the person who issued the book
    issued_to_id = models.CharField(max_length=90, null=True, blank=True)  # Stores student or faculty ID
    issue_date = models.DateField(null=True, blank=True)  # Original issue date
    return_date = models.DateField(auto_now=True)  # Automatically set to the current date when the record is created

    def __str__(self):
        return f"History: {self.book} issued to {self.issued_to_name}"
    


class Notice(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

