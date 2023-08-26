from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)
    publication_date = models.DateField()
    description = models.TextField()
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title

    def calculate_average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            total_ratings = sum(review.rating for review in reviews)
            self.average_rating = total_ratings / len(reviews)
            self.save()


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    text = models.TextField()

    def __str__(self):
        return f"{self.author.email}: {self.book.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.book.calculate_average_rating()

    
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.email}: {self.book.title}"
    
