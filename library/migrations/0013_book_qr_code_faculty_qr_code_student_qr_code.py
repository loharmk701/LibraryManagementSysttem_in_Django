# Generated by Django 5.1.5 on 2025-04-09 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0012_alter_book_isbn_alter_bookissuedhistory_book_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='qr_code',
            field=models.ImageField(blank=True, upload_to='qr_codes/books/'),
        ),
        migrations.AddField(
            model_name='faculty',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes/faculty/'),
        ),
        migrations.AddField(
            model_name='student',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes/students/'),
        ),
    ]
