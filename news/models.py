from django.db import models
from django.contrib.auth.models import User
from accounts.models import Author
from django.urls import reverse

class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f'{self.category_name}'

class Post(models.Model):
    paper = 'PA'
    news = 'NE'

    POST_TYPE = [
        (paper, 'Статья'),
        (news, 'Новость')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPE, default=paper)
    pub_time = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255, default='Введите название')
    text = models.TextField(default='Введите содержание')
    _rating = models.IntegerField(default=0)

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        self._rating = int(value) if value >= 0 else 0
        self.save()

    def like(self):
        self._rating += 1
        self.save()

    def dislike(self):
        self._rating += -1
        self.save()

    def preview(self):
        return f'{self.text[0:124]}...'

    def get_absolute_url(self):
        return reverse("post", kwargs={"pk": self.pk})

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default='Введите комментарий')
    pub_time = models.DateTimeField(auto_now_add=True)
    _rating = models.IntegerField(default=0)

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        self._rating = int(value) if value >= 0 else 0
        self.save()

    def like(self):
        self._rating += 1
        self.save()

    def dislike(self):
        self._rating += -1
        self.save()

