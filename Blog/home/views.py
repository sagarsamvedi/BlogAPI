from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Blog
from django.db.models import Q
from django.core.paginator import Paginator

class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            # Get the authenticated user
            user = request.user
            # Fetch blogs associated with the user
            blogs = user.blog.all()
            
            # If search query is provided, filter blogs based on title or content
            if request.GET.get('search'):
                search_query = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search_query) | Q(
                    content__icontains=search_query))
            
            # Serialize the blogs data
            serializer = BlogSerializer(blogs, many=True)

            return Response(
                {
                    'data': serializer.data,
                    'message': "Blogs fetched successfully"
                }, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {
                    'data': serializer.errors,
                    'message': "Something went wrong while fetching blogs"
                }, status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        try:
            # Extract data from the request
            data = request.data
            # Add the authenticated user to the data
            data['user'] = request.user.id
            # Serialize the data
            serializer = BlogSerializer(data=data)
            # Check if the data is valid
            if not serializer.is_valid():
                return Response(
                    {
                        'data': serializer.errors,
                        'message': "Failed to create a new blog"
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            # Save the serialized data to create a new blog
            serializer.save()

            return Response(
                {
                    'data': serializer.data,
                    'message': "Blog is created successfully"
                }, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {
                    'data': serializer.errors,
                    'message': "Something went wrong while creating a new blog"
                }, status=status.HTTP_400_BAD_REQUEST
            )

    def patch(self, request):
        try:
            # Extract data from the request
            data = request.data
            # Filter blogs based on the provided UID
            blog = Blog.objects.filter(uid=data.get('uid'))
            # Check if the blog exists
            if not blog.exists():
                 return Response(
                    {
                        'data': {},
                        'message': "Invalid Blog ID"
                    }, status=status.HTTP_404_NOT_FOUND
                )

            # Check if the authenticated user is the owner of the blog
            if request.user != blog[0].user:
                 return Response(
                    {
                        'data': {},
                        'message': "You are not an authorized user"
                    }, status=status.HTTP_401_UNAUTHORIZED
                )

             # Update the blog post
            serializer = BlogSerializer(blog[0], data=data, partial=True)
            # Check if the data is valid
            if not serializer.is_valid():
                return Response(
                    {
                        'data': serializer.errors,
                        'message': "Failed to update the blog post"
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            # Save the serialized data to update the blog post
            serializer.save()

            return Response(
                {
                    'data': serializer.data,
                    'message': "Blog post updated successfully"
                }, status=status.HTTP_200_OK
            )

        except Exception as e:
            print(e)
            return Response(
                {
                    'data': {},
                    'message': "Something went wrong while updating the blog post"
                }, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request):
        try:
            # Extract data from the request
            data = request.data
            # Filter blogs based on the provided UID
            blog = Blog.objects.filter(uid=data.get('uid'))
            # Check if the blog exists
            if not blog.exists():
                 return Response(
                    {
                        'data': {},
                        'message': "Invalid Blog ID"
                    }, status=status.HTTP_404_NOT_FOUND
                )

            # Check if the authenticated user is the owner of the blog
            if request.user != blog[0].user:
                 return Response(
                    {
                        'data': {},
                        'message': "You are not an authorized user"
                    }, status=status.HTTP_401_UNAUTHORIZED
                )

            # Delete the blog post
            blog[0].delete()
            return Response(
                    {
                        'data': {},
                        'message': "Blog deleted successfully"
                    }, status=status.HTTP_200_OK
                )

        except Exception as e:
            print(e)
            return Response(
                {
                    'data': {},
                    'message': "Something went wrong while deleting the blog post"
                }, status=status.HTTP_400_BAD_REQUEST
            )

# Public users can read random blogs
class PublicBlogView(APIView):

     def get(self, request):
        try:
            # Fetch all blog objects from the database and order them randomly 
            blogs = Blog.objects.all().order_by('?')

            # If search query is provided, filter blogs based on title or content
            if request.GET.get('search'):
                search_query = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search_query) | Q(
                    content__icontains=search_query))
            
            # Get the page number from the request, default is 1
            page_number = request.GET.get('page', 1)

            # Split the blog queryset and set the number of items per page (2 in this case)
            paginator = Paginator(blogs, 2)

            # Serialize the blogs for the requested page
            serializer = BlogSerializer(paginator.page(page_number), many=True)

            return Response(
                {
                    'data': serializer.data,
                    'message': "Blogs fetched successfully"
                }, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {
                    'data': {},
                    'message': "Something went wrong or you entered an invalid page"
                }, status=status.HTTP_400_BAD_REQUEST
            )
