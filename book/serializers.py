from rest_framework import serializers
from .models import Book, Author, Bookmark, Genre, Review
from django.contrib.auth.models import User


class BookAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


class BookSerializer(serializers.ModelSerializer):
    author = BookAuthorSerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Book
        fields = ['title', 'genre', 'author', 'average_rating']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = self.context.get('user')
        if user and user.is_authenticated:
            bookmarks = Bookmark.objects.filter(user=user, book=instance)
            representation['is_bookmarked'] = bookmarks.exists()
        return representation


class ReviewAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']
        

class ReviewSerializer(serializers.ModelSerializer):
    author = ReviewAuthorSerializer()
    
    class Meta:
        model = Review
        fields = ['author', 'rating', 'text']


class BookDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    author = BookAuthorSerializer()
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Book
        fields = ['title', 'genre', 'author', 'publication_date', 'description', 'average_rating', 'reviews']

        