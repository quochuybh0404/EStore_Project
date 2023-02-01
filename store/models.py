from email.policy import default
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length= 150, unique = True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete= models.PROTECT)
    name = models.CharField(max_length= 150, unique = True)
    image = models.ImageField(upload_to = 'store/images', default = 'store/images/default.png')

    def __str__(self):
        return self.name

class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete= models.PROTECT)
    name = models.CharField(max_length= 250)
    price = models.FloatField(default= 0.0)
    price_origin = models.FloatField(null = True)
    image = models.ImageField(upload_to = 'store/images', default = 'store/images/default.png')
    content = RichTextUploadingField(blank = True, null = True)
    public_day = models.DateTimeField(default = timezone.now)
    viewed = models.IntegerField(default= 0)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length= 100)
    email = models.EmailField(blank = False)
    subject = models.CharField(max_length = 100)
    message = models.TextField(blank = False)

    def __str__(self):
        return self.name




    