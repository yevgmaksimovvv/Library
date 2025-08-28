from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from core.models import Book, BorrowRecord
from datetime import date


class Command(BaseCommand):
    help = "Наполнение БД тестовыми данными (для использования отключить авто-поле!!)"

    def handle(self, *args, **kwargs):
        fake = Faker("ru_RU")
        for i in range(5):
            book = Book.objects.filter(available_copies__gt=1).order_by("?").first()
            if not book:
                self.stdout.write(self.style.ERROR("Нет свободных книг!"))
                return
            random_date = fake.date_time_between(
                start_date=date(2025, 1, 1), end_date=date(2025, 8, 27)
            )
            BorrowRecord.objects.create(
                book=book,
                borrower_name=fake.first_name(),
                borrow_date=timezone.make_aware(
                    random_date, timezone.get_current_timezone()
                ),
            )
            book.available_copies -= 1
            book.save()
        self.stdout.write(self.style.SUCCESS("Записи успешно сделаны!"))
