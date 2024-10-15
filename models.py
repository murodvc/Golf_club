from audioop import reverse

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.db import models

from blog.managers import CustomUserManager


# Create your models here.


class Eventss(models.Model):
    title = models.CharField(max_length=255,blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=300,blank=True)
    ticket = models.FloatField()
    imag = models.ImageField(upload_to='images/')
    date_joined = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, null=True, default=None, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("single_post", kwargs={"slug": self.slug})

    class Meta:
        ordering = ['-id']



class ClubHistory(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Founder(models.Model):
    name = models.CharField(max_length=100)
    club = models.ForeignKey('blog.ClubHistory', on_delete=models.CASCADE,related_name='founder')

    def __str__(self):
        return self.name

class CoFounder(models.Model):
    name = models.CharField(max_length=100)
    club = models.ForeignKey('blog.ClubHistory',on_delete=models.CASCADE, related_name='cofounder')

    def __str__(self):
        return self.name

class ImagesFounder(models.Model):
    image = models.ImageField(upload_to='image/')
    founder = models.ForeignKey('blog.Founder',on_delete=models.CASCADE, related_name='imagefounder')

class ImageCoFounder(models.Model):
    image = models.ImageField(upload_to='image/')
    cofounder = models.ForeignKey('blog.CoFounder',on_delete=models.CASCADE, related_name='imagecofounder')



class Email(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class MembershipComments(models.Model):
    full_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(unique=True)
    comment = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    class Meta:
        ordering = ['full_name']


class SendMessage(models.Model):
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name





class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        Group,
        related_name='blog_user_set',  # Specify a unique related_name
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='blog_user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='blog_user_set',  # Specify a unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='blog_user',
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'





