from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        all_posts = Post.objects.filter(author=self)
        posts_total = sum(elem.rating * 3 for elem in all_posts)
        comments_total = sum(elem.rating for elem in Comment.objects.filter(user=self.user)) \
                         + sum(elem.rating for elem in Comment.objects.filter(post__in=all_posts))

        self.rating = posts_total + comments_total


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    TYPES = [
        ('art', 'статья'),
        ('new', 'новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # on_delete - если автор удалён
    type = models.CharField(max_length=3, choices=TYPES, default='art')
    created = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=64, default='(без названия)')
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1

    def preview(self):
        return self.content[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # on_delete - если пост удалён
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # on_delete - если категория удалена


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # on_delete - если пользователь удалён
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1
