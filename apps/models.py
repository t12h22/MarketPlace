from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import os

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        # 画像ファイルの削除
        if self.image:
            # ファイルのフルパスを取得
            file_path = os.path.join(settings.MEDIA_ROOT, str(self.image))
            # ファイルを削除
            if os.path.exists(file_path):
                os.remove(file_path)
        super(Product, self).delete(*args, **kwargs)
