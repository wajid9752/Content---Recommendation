from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext as _
from django.core.validators import FileExtensionValidator

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(('email address'), unique=True)
    phone = models.CharField(max_length=20 , null=True , blank=True)
    otp = models.IntegerField(default=0)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    
    objects = CustomUserManager()
    
    def get_username(self):
        return self.email



class BaseClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(BaseClass):
    name = models.CharField(max_length=100 , help_text=_("Tag Name"))

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name    
    
class Category(BaseClass):
    name = models.CharField(max_length=100 , help_text=_("Category Name"))
    class Meta:
        ordering = ["name"]
    def __str__(self):
        return self.name        



class Content(BaseClass):
    user        = models.ForeignKey(CustomUser , on_delete=models.CASCADE , related_name= "my_contents")
    category    = models.ForeignKey(Category ,on_delete = models.CASCADE , related_name= "category_contents")
    title       = models.CharField(max_length=100 , help_text=_("Content Title") )
    description = models.TextField(help_text=_("Description of content you are adding"))
    file        = models.FileField(upload_to="content-files", 
                validators=[FileExtensionValidator(
                    allowed_extensions=['jpg', 'jpeg', 'png', 'mp4'])
                    ]
                    )
    tags        = models.ManyToManyField(Tag , related_name= "tag_contents")
    views       = models.PositiveIntegerField(default = 0)
    likes       = models.PositiveIntegerField(default=0)    
    dislikes    = models.PositiveIntegerField(default=0)    
    shares      = models.PositiveIntegerField(default=0) 
    
    def __str__(self):
        return self.title   

class Content_Attributes(BaseClass):
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE , related_name= "myaction")
    content_id = models.ForeignKey(Content , on_delete= models.CASCADE , related_name="attributes")
    is_like = models.BooleanField()
    def __str__(self):
        return str(self.user.email)   

    
class Content_Rating(BaseClass):
    user        = models.ForeignKey(CustomUser , on_delete=models.CASCADE , related_name= "rating_by")
    content_id = models.ForeignKey(Content , on_delete= models.CASCADE , related_name="ratings")
    rating = models.IntegerField(default=0)
       
    def __str__(self):
        return self.content_id.title +" rating : "+str(self.rating)   



