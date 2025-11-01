from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post
from .tasks import send_new_post_notification

@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers_m2m(sender, instance, action, **kwargs):
    if action == "post_add":
        print(f"🎯 M2M: категории добавлены к посту '{instance.title}'")
        categories = instance.categories.all()

        if categories.count() == 0:
            print("❌ Нет категорий - уведомления не отправляются")
            return

        send_new_post_notification.delay(instance.id)
        print(f"✅ Уведомления должны отправиться (Post ID: {instance.id})")