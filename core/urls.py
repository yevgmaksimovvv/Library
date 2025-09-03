from django.urls import path
from . import views

urlpatterns = [
    path("authors/", views.AuthorListCreateView.as_view(), name="author-list"),
    path("authors/<int:pk>/", views.AuthorDetailView.as_view(), name="author-detail"),
    path("books/", views.BookListCreateView.as_view(), name="book-list"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),
    path(
        "books/<int:pk>/uploadpdf/",
        views.BookUploadPDFView.as_view(),
        name="book-upload",
    ),
    path(
        "books/<int:pk>/downloadpdf/",
        views.BookDownloadPDFView.as_view(),
        name="book-download",
    ),
    path("borrow/", views.BorrowBook.as_view(), name="borrow-book"),
    path("borrow/<int:pk>/return/", views.ReturnBook.as_view(), name="return-book"),
]
