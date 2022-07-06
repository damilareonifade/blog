from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from core.settings import TIME_ZONE
from django.utils import timezone

def user_directory_path(instance,filename):
    return 'posts/%Y/%m/%d/'.format(instance.id, filename)

class Category(models.Model):
    name = models.CharField(max_length=250,help_text='Enter Your Category here')


    class Meta:
        verbose_name = ('Category')
        verbose_name_plural = ('Categories')
    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = (('drafts','drafts'),('Published','Published'))
    title = models.CharField(max_length=250)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    slug = models.SlugField(max_length=30)
    excerpt = models.CharField(max_length=200, blank=True, null = True)
    description = models.TextField()
    image = models.ImageField(
        upload_to=user_directory_path, default='posts/default.jpg')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='published')
    favourite= models.ManyToManyField(User,default=None,blank=True,related_name='favourites')
    like = models.ManyToManyField(User,related_name='like',default=None,blank=True)
    like_count = models.BigIntegerField(default = '0')
    thumbsup = models.IntegerField(default='0')
    thumbsdown = models.IntegerField(default='0')
    thumbs = models.ManyToManyField(User,related_name='thumbs', default='0',blank=True)

    created = models.DateTimeField(default= timezone.now)
    object = models.Manager() 
    
    def get_absolute_url(self):
        return reverse('blog:post_single', args=[self.slug])
    


    class Meta:
        verbose_name = ("Post")
        verbose_name_plural = ("Posts")

    def __str__(self):
        return self.title


class Comment(MPTTModel):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    parent = TreeForeignKey('self', on_delete=models.CASCADE,null=True, blank=True, related_name='children')
    content = models.TextField()
    author = models.ForeignKey(User,related_name='author',on_delete=models.CASCADE, default=None, blank=True,null=True)
    publish = models.DateTimeField(auto_now=timezone.now())
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment by {self.name}"
    class MPTTMeta:
        order_by_insertion = ['publish']

class Vote(models.Model):
    post = models.ForeignKey(Post, related_name = 'postid',default= None,blank=True,on_delete=models.CASCADE)
    user = models.ForeignKey(User,default = None,related_name='userid',blank=True,on_delete=models.CASCADE)
    vote = models.BooleanField(default =True)