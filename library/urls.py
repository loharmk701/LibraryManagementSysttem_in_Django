from django.urls import path
from . import views

urlpatterns = [
    # Dashboard (homepage)
    path('', views.dashboard, name='dashboard'),  # http://localhost:8000/

    # Book section
    path('books/', views.book_list, name='book-list'),  # http://localhost:8000/books/
    path('books/add/', views.book_form, name='book-add'),
    path('books/edit/<int:pk>/', views.book_form, name='book-edit'),
    path('books/delete/<int:pk>/', views.book_delete, name='book-delete'),

    # Students
    path('students/', views.student_list, name='student-list'),
    path('students/add/', views.student_form, name='student-add'),
    path('students/<int:pk>/edit/', views.student_form, name='student-edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student-delete'),

    # Faculty
    path('faculty/', views.faculty_list, name='faculty-list'),
    path('faculty/add/', views.faculty_form, name='faculty-add'),
    path('faculty/<int:pk>/edit/', views.faculty_form, name='faculty-edit'),
    path('faculty/<int:pk>/delete/', views.faculty_delete, name='faculty-delete'),

    # About page
    path('about/', views.About, name='About'),

    # Issue/Return books
    path('issued_books/', views.issued_books, name='issued_books'),
    path('issue_book_form/', views.issue_book_form, name='issue_book_form'),
    path('return_book/', views.return_book, name='return_book'),

    #issued with qrcode
    path('scan/', views.scan_page, name='scan_page'),
    path('issue-with-qrcode/', views.issued_book_with_qrcode, name='issued_book_with_qrcode'),
    path('api/get-book-id/', views.get_book_id_from_isbn, name='get_book_id_from_isbn'),
    path('api/get-person-id/', views.get_person_id_from_code, name='get_person_id_from_code'),  
]
