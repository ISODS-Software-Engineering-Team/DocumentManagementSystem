from django.contrib.auth.models import AbstractUser
from django.db import models
class Category(models.Model):
    category_id = models.CharField(max_length=20)
    category_name = models.CharField(max_length=70)

    def __str__(self):
        return self.category_id

    class Meta:
        db_table = 'Category'


class Document(models.Model):
    docs_id = models.CharField(max_length=50)
    category_id = models.CharField(max_length=20)
    brief = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    media_file = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    created_date = models.DateTimeField()
    def __str__(self):
        return self.docs_id

    class Meta:
        db_table = 'Document'

class User(AbstractUser):
    # Delete not use field
    username = None
    last_login = None
    is_staff = None
    is_superuser = None

    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email

    class Meta:
        db_table = 'User'
