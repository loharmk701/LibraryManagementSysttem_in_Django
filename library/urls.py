from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book-list'),  # This makes the root URL point to the book list page    
    path('book/add/', views.book_form, name='book-add'),  # Use book_form instead of book_add
    path('book/edit/<int:pk>/', views.book_form, name='book-edit'),  # Reuse book_form for editing
    path('book/delete/<int:pk>/', views.book_delete, name='book-delete'),
    #
    path('students/', views.student_list, name='student-list'),
    path('students/', views.student_list, name='student-list'),  # Student list view
    path('students/add/', views.student_form, name='student-add'),  # Add student view
    path('students/<int:pk>/edit/', views.student_form, name='student-edit'),  # Edit student view
    path('students/<int:pk>/delete/', views.student_delete, name='student-delete'),
    #
    path('faculty/', views.faculty_list, name='faculty-list'),
    path('faculty/add/', views.faculty_form, name='faculty-add'),  # Add this line for adding faculty
    path('faculty/<int:pk>/edit/', views.faculty_form, name='faculty-edit'),
    path('faculty/<int:pk>/delete/', views.faculty_delete, name='faculty-delete'),
    #
    path('About/', views.About, name='About'),
       #
    path('issued_books/', views.issued_books, name='issued_books'),
    path('issue_book_form/', views.issue_book_form, name='issue_book_form'),
    #
    path('return_book/', views.return_book, name='return_book'),
    #
    
    

]
