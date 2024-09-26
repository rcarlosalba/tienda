from django.core.management.base import BaseCommand
from inventory.models import Category, Product, ProductImage


class Command(BaseCommand):
    help = 'Clear all products, categories, and product images from the database'

    def handle(self, *args, **options):
        self.stdout.write(
            'Clearing all products, categories, and product images...')

        ProductImage.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All product images deleted.'))

        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All products deleted.'))

        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All categories deleted.'))

        self.stdout.write(self.style.SUCCESS('Database cleared successfully.'))
