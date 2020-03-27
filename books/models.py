from django.db import models
from users.models import User


class Genre(models.Model):
    genre = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'genres'

    def __str__(self):
        return self.genre


class Author(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'authors'

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    pages = models.IntegerField(blank=True)
    review = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    calification = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'books'

    def __str__(self):
        return self.title


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    num = models.PositiveIntegerField()
    text = models.FileField()
    pages = models.IntegerField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'chapters'

    def __str__(self):
        return self.title


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spoiler = models.BooleanField()

    def __str__(self):
        if len(self.text) > 50:
            frase = self.text[:50] + "..."
        else:
            frase = self.text
        return frase

