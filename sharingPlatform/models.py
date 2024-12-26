from django.db import models
from django.contrib.auth import get_user_model
import os

User = get_user_model()


# Create your models here.
class DatasetsCategory(models.Model):
    name = models.CharField(max_length=200)


class Dataset(models.Model):
    name = models.CharField(max_length=200)
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(DatasetsCategory, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='datasets/', default='path/to/default/file')

    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super(Dataset, self).delete(*args, **kwargs)

    class Meta:
        ordering = ['-pub_time']


class DatasetComment(models.Model):
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_time']
