from django.core.management.base import BaseCommand
from faker import Faker
from random import sample, randint, choice
from core.models import Author, Genre, Book


class Command(BaseCommand):
    help = "Наполнение БД тестовыми данными"

    def handle(self, *args, **kwargs):
        fake = Faker("ru_RU")
        authors = []
        genres = []
        for i in range(5):
            authors.append(
                Author.objects.create(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    bio=fake.text(max_nb_chars=100),
                    birth_date=fake.date_of_birth(minimum_age=50, maximum_age=400),
                )
            )
            genre = fake.word()
            while genre in Genre.objects.values_list("name", flat=True):
                genre = fake.word()
            genres.append(
                Genre.objects.create(name=genre, description=fake.text(max_nb_chars=50))
            )
        for i in range(10):
            available_copies = fake.random_int(min=2, max=50)
            rand_author = choice(authors)
            rand_genres = sample(genres, k=randint(1, 5))
            Book.objects.create(
                title=fake.word(),
                author=rand_author,
                summary=fake.text(max_nb_chars=100),
                isbn=fake.isbn13(),
                total_copies=available_copies + fake.random_int(min=1, max=5),
                available_copies=available_copies,
            ).genre.set(rand_genres)
        self.stdout.write(self.style.SUCCESS("Данные успешно загружены"))
