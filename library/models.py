import barcode
from barcode.writer import ImageWriter
from django.db import models
from io import BytesIO
from django.core.files import File
# Book model
import barcode
from barcode.writer import ImageWriter
from django.db import models
from io import BytesIO
from django.core.files import File
import qrcode
from django.core.files.base import ContentFile

import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    publisher = models.CharField(max_length=255)
    publication_date = models.DateField()
    quantity = models.IntegerField()
    qrcode = models.ImageField(upload_to='qrcodes/book/', blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Generate QR Code
        qr_data = f"Title: {self.title}\nAuthor: {self.author}\nISBN: {self.isbn}"
        qr = qrcode.make(qr_data)

        # Save QR Code to ImageField
        buffer = BytesIO()
        qr.save(buffer, format="png")
        self.qrcode.save(f"{self.isbn}_qrcode.png", ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)



# Student model
class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    student_id = models.CharField(max_length=12, unique=True)
    department = models.CharField(max_length=255)
    qrcode = models.ImageField(upload_to='qrcodes/student/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

    def save(self, *args, **kwargs):
        # Generate QR Code
        qr_data = f"First_name: {self.first_name}\nLast_nam:{self.last_name}\nStudent_id: {self.student_id}\nDepartment: {self.department}\nEmail: {self.email}"
        qr = qrcode.make(qr_data)

        # Save QR Code to ImageField
        buffer = BytesIO()
        qr.save(buffer, format="png")
        self.qrcode.save(f"{self.student_id}_qrcode.png", ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)
    

# Faculty model
class Faculty(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    faculty_id = models.CharField(max_length=10, unique=True)
    department = models.CharField(max_length=255)
    qrcode = models.ImageField(upload_to='qrcodes/faculty/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.faculty_id})"
    def save(self, *args, **kwargs):
        # Generate QR Code
        qr_data = f"First_name: {self.first_name}\nLast_nam:{self.last_name}\nStudent_id: {self.faculty_id}\nDepartment: {self.department}\nEmail: {self.email}"
        qr = qrcode.make(qr_data)

        # Save QR Code to ImageField
        buffer = BytesIO()
        qr.save(buffer, format="png")
        self.qrcode.save(f"{self.faculty_id}_qrcode.png", ContentFile(buffer.getvalue()), save=False)

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
