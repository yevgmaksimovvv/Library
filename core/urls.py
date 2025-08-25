from django.urls import path
from . import views

urlpatterns = [
    path("authors/", views.AuthorListCreateView.as_view(), name="author-list"),
    path("authors/<int:pk>/", views.AuthorDetailView.as_view(), name="author-detail"),
    path("genres/", views.GenreListCreateView.as_view(), name="genre-list"),
    path("genres/<int:pk>/", views.GenreDetailView.as_view(), name="genre-detail"),
    path("books/", views.BookListCreateView.as_view(), name="book-list"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),
    path(
        "borrow-records/",
        views.BorrowRecordListCreateView.as_view(),
        name="borrowrecord-list",
    ),
    path(
        "borrow-records/<int:pk>/",
        views.BorrowRecordDetailView.as_view(),
        name="borrowrecord-detail",
    ),
]
