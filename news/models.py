from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        from django.db.models import Sum

        post_rating = Post.objects.filter(author = self).aggregate(pr=Sum('rating'))['pr'] or 0
        post_rating *= 3

        comment_rating = self.user.comment_set.aggregate(cr=Sum('rating'))['cr'] or 0

        post_comment_rating = Comment.objects.filter(post__author=self).aggregate(pcr=Sum('rating'))['pcr'] or 0

        self.rating = post_rating + comment_rating + post_comment_rating
        self.save()

    def __str__(self):
        return self.user.username
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    POST_TYPES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=ARTICLE)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[:124] + '...' if len(self.content) > 124 else self.content

    def __str__(self):
        return self.title
class  PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
