from django.db import models
from django.contrib.auth.models import User
from image_cropping import ImageRatioField

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField( User, on_delete=models.CASCADE,related_name='profile')
    is_male = models.BooleanField(verbose_name='gender',choices=((False,'Female'),(True,'Male') ))
    pic = models.ImageField(upload_to = 'profiles/' )
    cropping = ImageRatioField('pic','400x400')
    about = models.TextField(max_length=2001)
    fb_link = models.URLField(max_length=100)

    def __str__(self):
        return self.user.username

class Category(models.Model):

    title = models.CharField(max_length=50)
    desc = models.TextField()
    pic = models.ImageField(upload_to = 'category/',blank=True, null=True)
    cropping = ImageRatioField('pic','750x400')

    def articles_num(self):
        return len(Article.objects.filter(category = self ))

    def __str__(self):
        return self.title


class Article(models.Model):
    slug = models.SlugField(max_length=100, unique = True)
    pub_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE) 
    category = models.ManyToManyField(Category,related_name='articles')
    title = models.CharField(unique=True,max_length=120)
    pic = models.ImageField(upload_to = 'blogs/' )
    cropping = ImageRatioField('pic','750x400')
    article = models.TextField()
    approved = models.BooleanField(default=False)
    
    def comments_num(self):
        return len(Comment.objects.filter(article = self ))

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='comments')
    comment = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment[:10]+' ...'