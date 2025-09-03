from rest_framework import serializers
from .models import Author, Genre, Book, BorrowRecord


# Доделать проверки на корректность данных!!
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), many=True, source="genre"
    )

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "summary",
            "isbn",
            "genre_ids",
            "total_copies",
            "available_copies",
            "content",
        ]


class BorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = "__all__"
