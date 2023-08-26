from django.contrib import admin
from .models import Book, Review, Genre, Author, Bookmark

# Register your models here.
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Bookmark)