from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)


class Book(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    summary = models.TextField(blank=True, null=True)
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.ManyToManyField(Genre, related_name="books")
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)


class BorrowRecord(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.PROTECT, related_name="borrow_records"
    )
    borrower_name = models.CharField(max_length=200)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    class Status(models.TextChoices):
        CHECKED_OUT = "checked_out", "Выдана"
        RETURNED = "returned", "Возвращена"

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CHECKED_OUT,
    )
