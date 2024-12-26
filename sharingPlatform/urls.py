from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'sharingPlatform'

urlpatterns = [
                  path('', views.index, name='index'),
                  path("dataset/details/<int:dataset_id>", views.dataset_details, name='dataset_details'),
                  path("dataset/pub", views.pub_dataset, name='pub_dataset'),
                  path("dataset/comment/pub", views.pub_comment, name="pub_comment"),
                  path("search", views.search, name="search"),
                  path("dataset/detail/download/<int:dataset_id>", views.download_dataset_file,
                       name="download_dataset_file"),
                  path("dataset/my_datasets", views.search_myself, name="search_myself"),
                  path("dataset/delete/<int:dataset_id>", views.dataset_delete, name="dataset_delete"),
                  path("dataset/edit/<int:dataset_id>", views.edit_dataset, name="dataset_edit")
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
