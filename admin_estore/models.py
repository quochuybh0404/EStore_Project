from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):
    # Tạo mối quan hệ từ class này tới bảng User
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    # Thêm một vài thuộc tính bạn muốn
    portfolio = models.URLField(blank=True)
    image = models.ImageField(upload_to = "users/", default = "users/no_avartar.png")

    def __str__(self):
        return self.user.username