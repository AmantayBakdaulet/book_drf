from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import BookFilter
from .serializers import BookSerializer, BookDetailSerializer
from .models import Book, Bookmark
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as drf_filters


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_bookmark(request, pk):
    """
    Toggle Bookmark for a Book.

    Toggle the bookmark status for a specific book. If the book is not bookmarked by the user,
    it will be bookmarked. If the book is already bookmarked, the bookmark will be removed.

    Args:
        pk (int): The ID of the book to toggle bookmark for.

    Returns:
        Response: A response indicating the bookmark status change.
    """
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    bookmark, created = Bookmark.objects.get_or_create(user=user, book=book)

    if not created:
        bookmark.delete()
        return Response({'message': f"Bookmark on {book.title} is deleted"})
    else:
        return Response({'message': f"{book.title} is bookmarked"})


class BookListView(generics.ListAPIView):
    """
    List of Books.

    Retrieve a paginated list of books, with the ability to search, filter, and order.

    - Supports search by title, author name, and genre name.
    - Supports filtering by genre, author, and publication date.
    - Supports ordering by average rating and publication date.

    Requires authentication.

    Returns:
        Response: A paginated list of books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class = BookFilter
    permission_classes = [IsAuthenticated]
    search_fields = ['title', 'author__name', 'genre__name']
    ordering_fields = ['average_rating', 'publication_date']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


class BookDetailView(generics.RetrieveAPIView):
    """
    Book Details.

    Retrieve detailed information about a specific book.

    Requires authentication.

    Returns:
        Response: Detailed information about the requested book.
    """
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer