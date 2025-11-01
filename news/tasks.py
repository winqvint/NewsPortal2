from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Post, Category
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_new_post_notification(post_id):
    try:
        post = Post.objects.get(id=post_id)
        categories = post.categories.all()

        for category in categories:
            subscribers = category.subscribers.all()

            for user in subscribers:
                if user.email:
                    html_content = render_to_string('account/email/new_post_notification.html', {
                        'post': post,
                        'user': user,
                        'category': category,
                    })

                    msg = EmailMultiAlternatives(
                        subject=f'Новая запись в разделе "{category.name}"',
                        body=f'Здравствуй, {user.username}. Новая статья в твоём любимом разделе!\n\n'
                             f'Заголовок: {post.title}\n'
                             f'Текст: {post.content[:50]}...\n\n'
                             f'Категория: {category.name}',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[user.email],
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

                    logger.info(f"Уведомление отправлено {user.email}")

    except Post.DoesNotExist:
        logger.error(f"Пост с ID {post_id} не найден")
    except Exception as e:
        logger.error(f"Ошибка отправки уведомления: {e}")


@shared_task
def send_weekly_digest():
    logger.info("Запуск еженедельной рассылки...")

    week_ago = timezone.now() - timedelta(days=7)
    total_emails = 0

    for category in Category.objects.all():
        new_posts = Post.objects.filter(
            categories=category,
            created_at__gte=week_ago
        ).order_by('-created_at')

        if not new_posts:
            continue

        subscribers = category.subscribers.all()

        for user in subscribers:
            if user.email:
                try:
                    html_content = render_to_string('account/email/weekly_digest.html', {
                        'user': user,
                        'category': category,
                        'posts': new_posts,
                        'week_ago': week_ago,
                    })

                    msg = EmailMultiAlternatives(
                        subject=f'📰 Еженедельная рассылка: {new_posts.count()} новых статей в разделе "{category.name}"',
                        body=f'Здравствуй, {user.username}!\n\n'
                             f'За неделю в разделе "{category.name}" появилось {new_posts.count()} новых статей.\n\n'
                             f'Читайте на нашем портале: http://127.0.0.1:8000/news/\n\n'
                             f'С уважением,\nNews Portal',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[user.email],
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

                    total_emails += 1
                    logger.info(f"Еженедельная рассылка отправлена {user.email}")

                except Exception as e:
                    logger.error(f"Ошибка еженедельной рассылки: {e}")

    logger.info(f"Еженедельная рассылка завершена. Отправлено писем: {total_emails}")
    return f"Отправлено писем: {total_emails}"