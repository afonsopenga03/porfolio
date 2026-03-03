# models.py

from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='projects'
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='images'
    )
    # FORÇAR o storage do Cloudinary diretamente no campo
    image = models.ImageField(
        upload_to='projects/',
        storage=MediaCloudinaryStorage(),
    )

    def __str__(self):
        return f"Imagem de {self.project.title}"
