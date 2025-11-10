from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import transaction


class Command(BaseCommand):
    help = 'Удаляет все статьи в указанной категории'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        # Получаем модели
        Post = apps.get_model('news', 'Post')
        Category = apps.get_model('news', 'Category')

        # Проверяем есть ли промежуточная модель PostCategory
        try:
            PostCategory = apps.get_model('news', 'PostCategory')
            has_post_category = True
        except LookupError:
            has_post_category = False

        category_name = options['category']

        # Подтверждение с более понятным форматом
        self.stdout.write(
            self.style.WARNING(
                f'\n⚠️  ВНИМАНИЕ: Вы собираетесь удалить все статьи из категории "{category_name}"'
            )
        )
        self.stdout.write(
            self.style.WARNING(
                '❗ Это действие нельзя отменить!'
            )
        )

        answer = input('❓ Подтвердите удаление [yes/NO]: ')

        # Более гибкая проверка подтверждения
        if answer.lower() not in ['yes', 'y', 'д', 'да']:
            self.stdout.write(self.style.ERROR('❌ Удаление отменено'))
            return

        try:
            category = Category.objects.get(name=category_name)

            # Определяем способ удаления в зависимости от структуры моделей
            if has_post_category:
                # Если есть промежуточная модель ManyToMany
                post_ids = PostCategory.objects.filter(category=category).values_list('post_id', flat=True)
                posts_count = len(post_ids)

                if posts_count == 0:
                    self.stdout.write(
                        self.style.WARNING(f'ℹ️ В категории "{category_name}" нет статей')
                    )
                    return

                # Удаляем в транзакции для безопасности
                with transaction.atomic():
                    Post.objects.filter(id__in=post_ids).delete()

            else:
                # Если связь напрямую через ForeignKey в Post
                posts_count = Post.objects.filter(category=category).count()

                if posts_count == 0:
                    self.stdout.write(
                        self.style.WARNING(f'ℹ️ В категории "{category_name}" нет статей')
                    )
                    return

                # Удаляем в транзакции
                with transaction.atomic():
                    Post.objects.filter(category=category).delete()

            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Успешно удалено {posts_count} статей из категории "{category_name}"'
                )
            )

        except Category.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ Категория "{category_name}" не найдена')
            )
            # Показываем доступные категории
            categories = Category.objects.all()
            if categories:
                self.stdout.write("📋 Доступные категории:")
                for cat in categories:
                    self.stdout.write(f"   - {cat.name}")