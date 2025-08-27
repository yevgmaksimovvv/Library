from rest_framework import generics, status
from .models import Author, Genre, Book, BorrowRecord
from .serializers import (
    AuthorSerializer,
    BookSerializer,
    BorrowRecordSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone


class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["author", "genre"]


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


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
