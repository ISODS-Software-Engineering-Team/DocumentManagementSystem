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

    def __all__(self):
        return self.docs_id, \
            self.category_id, \
            self.brief, \
            self.content, \
            self.media_file, \
            self.author, \
            self.created_date

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
        return self.is_superuser

    def __str__(self):
        return f'Email: {self.email}' f', ' \
               f'First Name: {self.first_name},' \
               f' Last Name: {self.last_name},' \
               f' Staff: {self.is_staff}'

    class Meta:
        db_table = 'User'


class Competition(models.Model):
    name = models.CharField(max_length=255)
    created_by_user = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    detail = models.TextField(max_length=10000, blank=True)

    """
     Requirement: User (the person who create the competition) have to upload 2 files:
     1. private test data: the original test ----- user must upload a file.
     2. training model: a model for competitor to download ----- user must upload a file.
     
     Requirement: Competitor (the person who compete with other) have to upload/download 2 files:
     1. competitor data: will be used to compare with original test ----- competitor must upload a file.
     2. data path: competitor will download the training model above ----- competitor will download a file. 
    """

    # test data field for user to upload test data
    private_test_data = models.FileField(upload_to="private_test", blank=True, null=True)

    # Training test model user must upload for competitor to download and train the model
    training_test_model = models.FileField(upload_to="models_training", blank=True)

    # Data field for competitors to upload data
    competitor_data = models.FileField(upload_to="competitor_data", blank=True)

    # Data path for competitors to download --> usually is an api
    data_path = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'Name: {self.name}' f', ' \
               f'Detail: {self.detail},' \
               f'Start at: {self.start_at},' \
               f'End at: {self.end_at}'

    @property
    def filename(self):
        return self.private_test_data.split('/')[-1:][0]

    def __all__(self):
        return self.name, \
            self.created_by_user, \
            self.start_at, \
            self.end_at, \
            self.detail, \
            self.private_test_data, \
            self.training_test_model, \
            self.competitor_data, \
            self.data_path

    class Meta:
        db_table = "Competition"


""" User_Competition model:
    store info of User who join the competition.
"""


class UserCompetition(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_date = models.DateTimeField(auto_now_add=True)
    result_path = models.CharField(max_length=500)
    public_score = models.IntegerField()
    private_score = models.IntegerField()

    class Meta:
        db_table = "User_Competition"

    def __str__(self):
        return f'User ID: {self.user_id}'f', ' \
               f'Competition ID: {self.competition_id}' f', ' \
               f'Joined Date: {self.joined_date}' f', '

    # Function to return public score
    def public_scores(self):
        return f'Public Score: {self.public_score}'f'.'

    # Function to return private score
    def private_scores(self):
        return f'Your Score: {self.private_score}' f'.'

