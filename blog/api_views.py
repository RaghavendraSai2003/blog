from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Post
from rest_framework import status
from .serializers import PostSerializer

#apis only for posts

@api_view(['GET'])
def get_posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_single_post(request, slug):
    try:
        post = Post.objects.get(slug=slug)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)
    
@api_view(['POST'])
def create_post(request):
    serializer = PostSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Post created", "data": serializer.data}, status=201)

    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_post(request, slug):
    try:
        post = Post.objects.get(slug=slug)
        post.delete()
        return Response({"message": "Post deleted"}, status=status.HTTP_204_NO_CONTENT)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "This is a protected view", "user": str(request.user)})
 