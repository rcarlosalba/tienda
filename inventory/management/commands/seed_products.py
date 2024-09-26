import requests
import uuid
import os
from django.core.management.base import BaseCommand
from inventory.models import Category, Product, ProductImage
from django.core.files.base import ContentFile
from requests.exceptions import RequestException
from django.conf import settings


class Command(BaseCommand):
    help = 'Seed the database with products from the Fake Store API'

    def download_image(self, url, max_retries=3):
        for attempt in range(max_retries):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                return response.content
            except RequestException as e:
                if attempt == max_retries - 1:
                    self.stdout.write(self.style.WARNING(
                        f"Failed to download image after {max_retries} attempts: {url}"))
                    return None
                time.sleep(1)  # Wait for 1 second before retrying

    def handle(self, *args, **options):
        api_url = 'https://fakestoreapi.com/products'
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            products_data = response.json()
            total_products = len(products_data)
            self.stdout.write(self.style.SUCCESS(
                f'Successfully fetched {total_products} products from the API'))
        except RequestException as e:
            self.stdout.write(self.style.ERROR(
                f'Failed to fetch products from the API: {str(e)}'))
            return

        success_count = 0
        error_count = 0

        for index, product_data in enumerate(products_data, start=1):
            self.stdout.write(
                f'Processing product {index} of {total_products}')

            category, _ = Category.objects.get_or_create(
                name=product_data['category'])

            unique_code = str(uuid.uuid4())[:8]

            product, created = Product.objects.get_or_create(
                name=product_data['title'],
                defaults={
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'category': category,
                    'stock': 10,
                    'code': unique_code
                }
            )

            if created:
                image_url = product_data['image']
                image_content = self.download_image(image_url)
                if image_content:
                    product_image = ProductImage(product=product)
                    image_name = f"{product.name.replace(' ', '_')}_{product.id}.jpg"
                    # Guardamos directamente el nombre del archivo, sin incluir 'products_images/'
                    product_image.image.save(
                        image_name,
                        ContentFile(image_content),
                        save=True
                    )
                    self.stdout.write(self.style.SUCCESS(
                        f'Successfully created product: {product.name} with code: {product.code} and image'))
                    success_count += 1
                else:
                    self.stdout.write(self.style.WARNING(
                        f'Created product: {product.name} with code: {product.code} but failed to download image'))
                    error_count += 1
            else:
                self.stdout.write(self.style.WARNING(
                    f'Product already exists: {product.name}'))
                error_count += 1

            if index % 5 == 0:
                self.stdout.write(self.style.SUCCESS(
                    f'Progress: {index}/{total_products} products processed. Successes: {success_count}, Errors: {error_count}'))

        self.stdout.write(self.style.SUCCESS(
            f'Seeding completed. Total products: {total_products}, Successes: {success_count}, Errors: {error_count}'))
