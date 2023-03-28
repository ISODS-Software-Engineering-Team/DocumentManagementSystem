from django.contrib.auth.models import AbstractUser, BaseUserManager
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

    # Add image field, set it to null, blank to null
    document_image = models.ImageField(upload_to='document_images', null=True, blank=True)
    def __str__(self):
        return self.docs_id

    class Meta:
        db_table = 'Document'

class User(AbstractUser):
    # Delete not use field
    username = models.CharField(max_length=100)

    # Regular register will make a user is_user
    # Register a user by admin will make a user is staff.
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']

    @staticmethod
    def has_perms(perm, obj=None):
        return True

    @property
    def is_admin(self):
        return self.admin

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'User'
