from django.contrib import admin
from .models import Dataset, DatasetComment, DatasetsCategory


# Register your models here.


class DatasetsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class DatasetAdmin(admin.ModelAdmin):
    list_display = ['name', 'content', 'pub_time', 'category', 'author']


class DatasetCommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'dataset', 'pub_time', 'author']


admin.site.register(Dataset, DatasetAdmin)
admin.site.register(DatasetComment, DatasetCommentAdmin)
admin.site.register(DatasetsCategory, DatasetsCategoryAdmin)
