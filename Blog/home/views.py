from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Blog
from django.db.models import Q
from django.core.paginator import Paginator
# from django.contrib.auth.models import User


class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            user = request.user
            blogs = user.blog.all()
            if request.GET.get('search'):
                search_query = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search_query) | Q(
                    content__icontains=search_query))
            serializer = BlogSerializer(blogs, many=True)

            return Response(
                {
                    'data': serializer.data,
                    'message': "Blogs fetched cuccessfully"
                }, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {
                    'data': serializer.errors,
                    'message': "Something went wrong while creating blog"
                }, status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        try:
            data = request.data
            data['user'] = request.user.id
            serializer = BlogSerializer(data=data)
            if not serializer.is_valid():
                return Response(
                    {
                        'data': serializer.errors,
                        'message': "Failed to create new blog"
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()

            return Response(
                {
                    'data': serializer.data,
                    'message': "Blog is created cuccessfully"
                }, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {
                    'data': serializer.errors,
                    'message': "Something went wrong while fetching blog"
                }, status=status.HTTP_400_BAD_REQUEST
            )

    def patch(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid=data.get('uid'))
            if not blog.exists():
                 return Response(
                    {
                        'data': {},
                        'message': "Invalid Blog id"
                    }, status=status.HTTP_404_NOT_FOUND
                )

            if request.user != blog[0].user:
                 return Response(
                    {
                        'data': {},
                        'message': "You are not authorized user"
                    }, status=status.HTTP_401_UNAUTHORIZED
                )

             # Update the blog post
            serializer = BlogSerializer(blog[0], data=data, partial=True)
            if not serializer.is_valid():
                return Response(
                    {
                        'data': serializer.errors,
                        'message': "Failed to update the blog post"
                    }, status=status.HTTP_400_BAD_REQUEST
                )
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
            data = request.data
            blog = Blog.objects.filter(uid = data.get('uid'))
            if not blog.exists():
                 return Response(
                    {
                        'data': {},
                        'message': "Invalid Blog id"
                    }, status=status.HTTP_404_NOT_FOUND
                )

            if request.user != blog[0].user:
                 return Response(
                    {
                        'data': {},
                        'message': "You are not authorized user"
                    }, status=status.HTTP_401_UNAUTHORIZED
                )

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
            # fetches all blog objects from the database and orders them randomly 
            blogs = Blog.objects.all().order_by('?')

            if request.GET.get('search'):
                search_query = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search_query) | Q(
                    content__icontains=search_query))
            
    
            page_number = request.GET.get('page',1)

            # splitting the blog query set and setting number of items per page (2 IN THIS CASE)
            paginator = Paginator(blogs,2)

            # serializing the blogs for the requested page
            serializer =BlogSerializer(paginator.page(page_number),many = True)

            return Response(
                {
                    'data': serializer.data,
                    'message': "Blogs fetched cuccessfully"
                }, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {
                    'data': {},
                    'message': "Something went wrong or you entered invalid page"
                }, status=status.HTTP_400_BAD_REQUEST
            )
