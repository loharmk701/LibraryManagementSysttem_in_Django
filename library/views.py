from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Book, Student, Faculty, IssuedBook, BookIssuedHistory
from .forms import BookForm, StudentForm, FacultyForm

# ------------------- BOOK VIEWS -------------------

def book_list(request):
    """Display a list of books sorted alphabetically by title."""
    books = Book.objects.all().order_by('title')
    return render(request, 'library/book_list.html', {'books': books})

def book_form(request, pk=None):
    """Handles both adding and editing a book."""
    book = get_object_or_404(Book, pk=pk) if pk else None
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'library/book_form.html', {'form': form})

def book_delete(request, pk):
    """Handles book deletion."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'library/book_confirm_delete.html', {'book': book})

# ------------------- STUDENT VIEWS -------------------

def student_list(request):
    """Display a list of students sorted alphabetically by first name."""
    students = Student.objects.all().order_by('first_name')
    return render(request, 'library/student_list.html', {'students': students})

def student_form(request, pk=None):
    """Handles both adding and editing a student."""
    student = get_object_or_404(Student, pk=pk) if pk else None
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student-list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'library/student_form.html', {'form': form})

def student_delete(request, pk):
    """Handles student deletion."""
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect('student-list')

# ------------------- FACULTY VIEWS -------------------

def faculty_list(request):
    """Display a list of faculty members sorted alphabetically by first name."""
    faculty_members = Faculty.objects.all().order_by('first_name')
    return render(request, 'library/faculty_list.html', {'faculty_members': faculty_members})

def faculty_form(request, pk=None):
    """Handles both adding and editing a faculty member."""
    faculty = get_object_or_404(Faculty, pk=pk) if pk else None
    if request.method == 'POST':
        form = FacultyForm(request.POST, instance=faculty)
        if form.is_valid():
            form.save()
            return redirect('faculty-list')
    else:
        form = FacultyForm(instance=faculty)
    return render(request, 'library/faculty_form.html', {'form': form})

def faculty_delete(request, pk):
    """Handles faculty deletion."""
    faculty = get_object_or_404(Faculty, pk=pk)
    if request.method == 'POST':
        faculty.delete()
        return redirect('faculty-list')
    return render(request, 'library/faculty_confirm_delete.html', {'faculty': faculty})

# ------------------- BOOK ISSUING & RETURN -------------------

def issued_books(request):
    """List all issued books and mark overdue ones."""
    issued_books = IssuedBook.objects.all()
    today = timezone.now().date()
    for issued_book in issued_books:
        issued_book.is_overdue = issued_book.return_date < today if issued_book.return_date else False
    return render(request, 'library/issued_books.html', {'issued_books': issued_books})

def issue_book_form(request):
    """Handles book issuance to students or faculty."""
    if request.method == 'POST':
        if request.POST.get('password') != 'ict124':
            messages.error(request, "Incorrect password.")
            return redirect('issue_book_form')
        
        book = get_object_or_404(Book, id=request.POST.get('book'))
        if book.quantity < 1:
            messages.error(request, f"The book '{book.title}' is not available for issuing.")
            return redirect('issue_book_form')
        
        issue_date = datetime.strptime(request.POST.get('issue_date'), '%Y-%m-%d').date()
        return_date = issue_date + timedelta(days=15)
        issued_to_role = request.POST.get('issued_to_role')
        issued_to = get_object_or_404(Student if issued_to_role == 'student' else Faculty, id=request.POST.get('issued_to'))
        
        IssuedBook.objects.create(book=book, issued_to_student=issued_to if issued_to_role == 'student' else None, issued_to_faculty=issued_to if issued_to_role == 'faculty' else None, issue_date=issue_date, return_date=return_date)
        book.quantity -= 1
        book.save()
        messages.success(request, f"The book '{book.title}' has been issued successfully.")
        return redirect('issued_books')

    return render(request, 'library/issue_book_form.html', {
        'books': Book.objects.all().order_by('title'),
        'students': Student.objects.all().order_by('first_name', 'last_name'),
        'faculties': Faculty.objects.all().order_by('first_name', 'last_name')
    })

def return_book(request):
    """Handles book returns and updates history."""
    if request.method == 'POST' and request.POST.get('password') == 'ict124':
        issued_book = get_object_or_404(IssuedBook, id=request.POST.get('issued_book'), returned=False)
        issued_book.book.quantity += 1
        issued_book.book.save()
        issued_to = issued_book.issued_to_student or issued_book.issued_to_faculty
        BookIssuedHistory.objects.create(
            issued_book_id=str(issued_book.id),
            book=issued_book.book.title,
            issued_to_student_faculty='Student' if issued_book.issued_to_student else 'Faculty',
            issued_to_name=f"{issued_to.first_name} {issued_to.last_name}",
            issued_to_id=issued_to.id,
            issue_date=issued_book.issue_date,
            return_date=datetime.now()
        )
        issued_book.delete()
        messages.success(request, f'Book "{issued_book.book.title}" has been successfully returned.')
        return redirect('return_book')
    
    return render(request, 'library/return_book.html', {'issued_books': IssuedBook.objects.filter(returned=False)})

def About(request):
    """Displays the About page."""
    return render(request, 'library/About.html')
#--------------------------------------------------------------------------------------------#

from .models import Notice
def dashboard(request):
    context = {
        'total_books': Book.objects.count(),
        'issued_books': IssuedBook.objects.count(),
        'total_students': Student.objects.count(),
        'total_faculty': Faculty.objects.count(),
        'notices': Notice.objects.order_by('-created_at')[:5],  # Show latest 5 notices
    }
    return render(request, 'library\dashboard.html',context)
#-------------------------------------------------------------------------------------------------------------------------------------------------
from django.http import JsonResponse
import json
from datetime import date, timedelta

def issued_book_with_qrcode(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        person_id = data.get('person_id')  # GTU Enrollment or Karmayogi ID
        book_id = data.get('book_id')      # Book ID (QR)

        try:
            book = Book.objects.get(book_id=book_id)
        except Book.DoesNotExist:
            return JsonResponse({'message': 'Book not found'}, status=404)

        issue_date = date.today()
        return_date = issue_date + timedelta(days=14)

        # Try to find the person as a Student first
        student = Student.objects.filter(student_id=person_id).first()
        if student:
            IssuedBook.objects.create(
                book=book,
                issued_to_student=student,
                issue_date=issue_date,
                return_date=return_date
            )
            return JsonResponse({'message': f'Book issued to student {student.first_name}'})

        # If not a student, try to find as Faculty
        faculty = Faculty.objects.filter(faculty_id=person_id).first()
        if faculty:
            IssuedBook.objects.create(
                book=book,
                issued_to_faculty=faculty,
                issue_date=issue_date,
                return_date=return_date
            )
            return JsonResponse({'message': f'Book issued to faculty {faculty.first_name}'})

        return JsonResponse({'message': 'No matching student or faculty found'}, status=404)
#==========================================================================================================
from django.shortcuts import render

def scan_page(request):
    return render(request, 'library/scan_issue.html')
#-------------------------------------------------------------
def get_book_id_from_isbn(request):
    isbn = request.GET.get('isbn')
    try:
        book = Book.objects.get(isbn=isbn)
        return JsonResponse({'book_id': book.id})
    except Book.DoesNotExist:
        return JsonResponse({'book_id': None})

def get_person_id_from_code(request):
    code = request.GET.get('code')
    student = Student.objects.filter(student_id=code).first()
    if student:
        return JsonResponse({'id': student.id, 'role': 'student'})
    faculty = Faculty.objects.filter(faculty_id=code).first()
    if faculty:
        return JsonResponse({'id': faculty.id, 'role': 'faculty'})
    return JsonResponse({'id': None, 'role': None})

