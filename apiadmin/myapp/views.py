from django.shortcuts import render ,get_object_or_404
from .models import Category, Article, User, Comment
from rest_framework import viewsets, status, permissions, generics
from rest_framework.response import Response
from .serializers import CategorySerializer, ArticleSerializer, UserSerializer, ArticleSerializer_create
from rest_framework.views import APIView
from django.http.response import HttpResponse, HttpResponseForbidden
# Our rest_framework permissions here.

def is_auth(request):
    return HttpResponse(content=  'is_staff '+str(request.user.is_staff))
    



class ApprovedOrOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return bool(obj.approved)
        return ( request.user.id is obj.user ) or request.user.is_staff or obj.approved



class IsAdminOrReadOnly_Category(permissions.BasePermission):
    def has_permission(self, request,view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff



class IsOwnerOrReadOnly_User(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS) and request.user:
            return True
        return ( request.user == obj ) and request.user.is_staff










class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly_Category,)


class ArticleList(APIView):
    serializer_class = ArticleSerializer_create
    def get(self, request, format=None):
        if request.user.is_staff:
            articles = Article.objects.all()
        else :
            articles = Article.objects.filter(approved=True)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ArticleDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    permission_classes = [ApprovedOrOwnerOrAdmin]
    def get_object(self, pk, request):
        article = get_object_or_404( Article, pk=pk)
        self.check_object_permissions(self.request, article)
        return article

    def get(self, request, pk, format=None):
        article = self.get_object(pk, request)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        article = self.get_object(pk, request)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        article = self.get_object(pk, request)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly_User,)