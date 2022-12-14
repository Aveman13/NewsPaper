from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    _rating = models.IntegerField(default=0)

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        self._rating = int(value) if value >= 0 else 0
        self.save()

    def update_rating(self):
        from news.models import Comment, Post
        self._rating = 0
        for comment in Comment.objects.filter(user=self.user):
            self._rating += comment.rating

        for post in Post.objects.filter(author=Author.objects.get(user=self.user)):
            self._rating += post.rating * 3
            for comments_to_post in Comment.objects.filter(post=post):
                self._rating += comments_to_post.rating
        self.save()

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'

