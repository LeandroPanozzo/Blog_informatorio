from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Comment(models.Model):
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    

    def __str__(self):
        return f'{self.author.username} - {self.content}'
class Post(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha_posteo = models.DateTimeField(default=timezone.now)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes/', blank=True, null=True)

    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def get_comments(self):
        return self.comments.all()  # Access related comments

class Denuncia(models.Model):
    post = models.ForeignKey('Spa.Post', on_delete=models.CASCADE, related_name='denuncias')
    denunciante = models.ForeignKey(User, on_delete=models.CASCADE)
    motivo = models.TextField(null=False, blank=False)  
    fecha_denuncia = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='pendiente')
    
    def __str__(self):
        return f'Denuncia sobre "{self.post.titulo}" por {self.denunciante.username}'

# Create your models here.
