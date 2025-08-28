from django.core.management.base import BaseCommand
from core.models import BorrowRecord
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = "Данные о задержанных более, чем на 14 дней, книгах"

    def handle(self, *args, **kwargs):
        for record in BorrowRecord.objects.filter(
            borrow_date__lte=(timezone.now() - timedelta(days=14))
        ):
            for field in record.book._meta.get_fields():
                text = getattr(record.book, field.name)
                print(f"{field.name}: {text}", end="  ")
            print(record.borrower_name)

        self.stdout.write(self.style.SUCCESS("Данные успешно распечатаны"))
