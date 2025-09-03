from rest_framework import generics, status
from .models import Author, Book, BorrowRecord
from .serializers import (
    AuthorSerializer,
    BookSerializer,
    BorrowRecordSerializer,
)

# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.core.cache import cache
from django.http import FileResponse
from io import BytesIO


# from .utils import convert_pdf_to_text


class AuthorListCreateView(generics.ListCreateAPIView):
    serializer_class = AuthorSerializer

    def get_queryset(self):
        cache_key = "authors_list"
        cached_authors = cache.get(cache_key)
        if cached_authors:
            return cached_authors
        authors = Author.objects.all()
        cache.set(cache_key, authors, timeout=60 * 2)
        return authors


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookListCreateView(generics.ListCreateAPIView):
    # queryset = Book.objects.all()
    serializer_class = BookSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ["author", "genre"]

    def get_queryset(self):
        authors = self.request.query_params.getlist("author", None)
        genres = self.request.query_params.getlist("genre", None)
        cache_key = (
            f"book_list_author_{authors}_genre_{genres}"
            if (authors or genres)
            else "book_list"
        )
        cached_books = cache.get(cache_key)

        print("Cached books:", cached_books)
        if cached_books:
            return cached_books
        print("Querying DB...")

        books = Book.objects.all()
        if authors:
            books = books.filter(author_id__in=authors)
        if genres:
            books = books.filter(genre__id__in=genres).distinct()

        cache.set(cache_key, books, 60 * 10)

        return books

    def perform_create(self, serializer):
        serializer.save()
        cache.delete_pattern("book_list*")


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookUploadPDFView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def patch(self, request, *args, **kwargs):
        book = self.get_object()

        if not "content" in request.FILES:
            return Response(
                {"detail": "Не найден PDF файл"}, status=status.HTTP_400_BAD_REQUEST
            )
        uploaded_file = request.FILES["content"]

        if not uploaded_file.content_type == "application/pdf":
            return Response(
                {"detail": "Файл должен быть PDF"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        book.content = uploaded_file.read()
        book.save()
        return Response({"detail": "PDF успешно загружен."}, status=status.HTTP_200_OK)


class BookDownloadPDFView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def retrieve(self, request, *args, **kwargs):
        book = self.get_object()
        if not book.content:
            return Response(
                {"error": "Нет PDF файла"}, status=status.HTTP_404_NOT_FOUND
            )
        pdf_file = BytesIO(book.content)
        response = FileResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{book.title}.pdf"'
        return response


class BorrowBook(APIView):
    def post(self, request):
        book_id = request.data.get("book_id")
        borrower_name = request.data.get("borrower_name")

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "Книга не найдена"}, status=status.HTTP_404_NOT_FOUND
            )
        if book.available_copies < 1:
            return Response(
                {"error": "Нет доступных книг"}, status=status.HTTP_400_BAD_REQUEST
            )

        borrow_record = BorrowRecord.objects.create(
            book=book, borrower_name=borrower_name
        )

        book.available_copies -= 1
        book.save()

        return Response(
            BorrowRecordSerializer(borrow_record).data, status=status.HTTP_201_CREATED
        )


class ReturnBook(APIView):
    def post(self, request, pk):
        try:
            borrow_record = BorrowRecord.objects.get(id=pk)
        except BorrowRecord.DoesNotExist:
            return Response(
                {"error": "Записи о выдаче не существует"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if borrow_record.status == BorrowRecord.Status.RETURNED:
            return Response(
                {"error": "Книга уже возвращена"}, status=status.HTTP_400_BAD_REQUEST
            )

        borrow_record.status = BorrowRecord.Status.RETURNED
        borrow_record.return_date = timezone.now()
        borrow_record.save()

        book = borrow_record.book
        book.available_copies += 1
        book.save()

        return Response(
            BorrowRecordSerializer(borrow_record).data, status=status.HTTP_200_OK
        )
