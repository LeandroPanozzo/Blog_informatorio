from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from users.forms import CommentForm  # Ensure this path is correct

from .models import Denuncia, Post, Comment
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.urls import reverse


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['titulo', 'contenido', 'imagen']
    template_name = 'Spa/post_form.html'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.autor

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('Inicio-Spa')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.autor or self.request.user.is_staff


class RemoveImageView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return self.request.user == post.autor

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if post.imagen:
            post.imagen.delete()
            post.imagen = None
            post.save()
            messages.success(request, "La imagen ha sido eliminada.")
        else:
            messages.warning(request, "No hay imagen para eliminar.")
        return redirect('post-update', pk=post.pk)
# Verifica si el usuario es administrador
def is_admin(user):
    return user.is_superuser or user.is_staff
@user_passes_test(lambda u: u.is_superuser)
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    usuario.delete()
    messages.success(request, 'El usuario ha sido eliminado.')
    return redirect('Inicio-Spa')  # Redirige a la página de inicio
@user_passes_test(lambda u: u.is_superuser)
def eliminar_denuncia(request, pk):
    denuncia = get_object_or_404(Denuncia, pk=pk)
    denuncia.delete()
    messages.success(request, 'La denuncia ha sido eliminada.')
    return redirect('Inicio-Spa')  # Redirige a la vista de denuncias después de eliminar
@user_passes_test(lambda u: u.is_superuser)
def resolver_denuncia(request, pk):
    denuncia = get_object_or_404(Denuncia, pk=pk)  # Obtén la denuncia específica
    return render(request, 'spa/resolver_denuncia.html', {'denuncia': denuncia})
@user_passes_test(lambda u: u.is_superuser)  # Solo permite a los administradores
def view_denuncias(request):
    denuncias = Denuncia.objects.all()  # Obtén todas las denuncias
    return render(request, 'spa/view_denuncias.html', {'denuncias': denuncias})
@user_passes_test(lambda u: u.is_superuser)  # Solo permite a los administradores
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post-list')  # Cambia 'post-list' por el nombre de la URL a la que deseas redirigir.
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('Inicio-Spa')  # Redirige a la página principal o a donde prefieras
    return redirect('Inicio-Spa')  # Redirección en caso de que no sea un POST
@user_passes_test(is_admin)
def eliminar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()  # Elimina la publicación
    messages.success(request, 'Publicación eliminada con éxito.')  # Mensaje de éxito
    return redirect('Inicio-Spa')  # Redirige a la página de inicio o a donde desees

def home(request):
    
    context ={
        
        'posts':Post.objects.all()
    }
    return render(request, 'spa/home.html', context)

class PostListView(ListView):
    model=Post
    template_name= 'Spa/home.html'
    context_object_name= 'posts'
    ordering=['-fecha_posteo']
    paginate_by=5
    
#ver los post del usuario
class UserPostListView(ListView):
    model=Post
    template_name= 'Spa/user_posts.html'
    context_object_name= 'posts'
    ordering=['-fecha_posteo']
    paginate_by=5   
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(autor=user).order_by('fecha_posteo')

class PostDetailView(DetailView):
    model = Post
    template_name = 'spa/post_detail.html'  # Adjust to your template's path
    context_object_name = 'object'  # or whatever you named your post in the template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()  # Fetch comments related to the post
        context['comment_form'] = CommentForm()  # Include the comment form
        return context
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['titulo', 'contenido', 'imagen']  # Agrega 'imagen' aquí
    template_name = 'Spa/post_form.html'  # Asegúrate de que esta plantilla exista

    def form_valid(self, form):
        form.instance.autor = self.request.user  # Asigna el autor
        return super().form_valid(form)  # Esto llama a get_success_url

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})  # Usa self.object.pk aquí


def about(request):
    return render(request, 'spa/About.html', {'title': 'about'})
# Create your views here.
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('Inicio-Spa')

    def test_func(self):
        post = self.get_object()
        # Solo permitir al autor o al staff eliminar el post
        if self.request.user == post.autor or self.request.user.is_staff:
            return True
        return False


# Vista para gestionar denuncias (solo accesible para personal)
@staff_member_required
def gestionar_denuncias(request):
    denuncias = Denuncia.objects.filter(estado='pendiente')
    context = {
        'denuncias': denuncias
    }
    return render(request, 'spa/gestionar_denuncias.html', context)

# Vista para resolver una denuncia específica (solo usuarios autenticados)
@login_required
def resolver_denuncia(request, pk):
    denuncia = get_object_or_404(Denuncia, pk=pk)
    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'bloquear_usuario':
            denuncia.post.autor.is_active = False
            denuncia.post.autor.save()
        elif accion == 'emitir_advertencia':
            # Lógica para enviar una advertencia al usuario
            pass
        denuncia.estado = 'revisado'
        denuncia.save()
        return redirect('gestionar-denuncias')
    return render(request, 'spa/resolver_denuncia.html', {'denuncia': denuncia})

@login_required
def crear_denuncia(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        motivo = request.POST.get('motivo')
        if motivo:  # Verificamos que el motivo esté presente
            Denuncia.objects.create(post=post, denunciante=request.user, motivo=motivo)
            return redirect('post-detail', pk=post.pk)
        else:
            # Maneja el caso donde no se envía un motivo
            return render(request, 'spa/crear_denuncia.html', {'post': post, 'error': 'Debes proporcionar un motivo.'})

    return render(request, 'spa/crear_denuncia.html', {'post': post})
@login_required
def home(request):
    context = {
        'is_admin': request.user.is_superuser or request.user.is_staff,  # Verifica si el usuario es admin
        # Agrega otros elementos del contexto según sea necesario
    }
    return render(request, 'home.html', context)  # Cambia 'home.html' por tu plantilla correspondiente
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        parent_comment_id = request.POST.get('parent_comment_id')  # Obtener el ID del comentario padre si existe

        if content:  # Asegurarse de que el contenido no esté vacío
            if parent_comment_id:
                # Si hay un comentario padre, creamos una respuesta
                parent_comment = get_object_or_404(Comment, id=parent_comment_id)
                comment = Comment(post=post, author=request.user, content=content, parent_comment=parent_comment)  # Cambiado a parent_comment
            else:
                # Si no hay un comentario padre, creamos un nuevo comentario
                comment = Comment(post=post, author=request.user, content=content)

            comment.save()  # Guardamos el comentario o la respuesta
            messages.success(request, "Tu comentario ha sido agregado.")
        else:
            messages.error(request, "No puedes enviar un comentario vacío.")

        return redirect('post-detail', post_id=post.id)  # Redirige a la página del post
    
    return redirect('post-detail', post_id=post.id)  # Redirige si no es un POST

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Solo el autor o un administrador puede eliminar el comentario
    if comment.author == request.user or request.user.is_superuser:
        comment.delete()
        messages.success(request, "Comentario eliminado con éxito.")
    else:
        messages.error(request, "No tienes permiso para eliminar este comentario.")
    
    return redirect('post-detail', pk=comment.post.id)  # Asegúrate de que 'post-detail' esté definido
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Obtiene todos los comentarios principales relacionados con el post
    comments = Comment.objects.filter(post=post, parent_comment=None).prefetch_related('replies')
    comment_form = CommentForm()

    if request.method == 'POST':
        # Manejo de la creación de un nuevo comentario o respuesta
        content = request.POST.get('content')
        parent_comment_id = request.POST.get('parent_comment_id')  # ID del comentario padre si existe

        if parent_comment_id:
            # Si hay un comentario padre, crea una respuesta
            parent_comment = get_object_or_404(Comment, id=parent_comment_id)
            comment = Comment(post=post, author=request.user, content=content, parent_comment=parent_comment)
        else:
            # Si no hay un comentario padre, crea un nuevo comentario
            comment = Comment(post=post, author=request.user, content=content)

        comment.save()
        return redirect('post-detail', post_id=post_id)  # Redirige a la misma página después de guardar

    context = {
        'object': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'post-detail.html', context)

@login_required  # Requiere que el usuario esté autenticado
def user_posts(request):
    # Obtén los posts del usuario autenticado
    posts = Post.objects.filter(autor=request.user)  # Cambia 'autor' si es necesario
    return render(request, 'Spa/user_posts.html', {'posts': posts})
@login_required
def mis_posts(request):
    posts = Post.objects.filter(autor=request.user)  # Cambia 'autor' si es necesario
    return render(request, 'Spa/mis_posts.html', {'posts': posts})
def faq_view(request):
    return render(request, 'Spa/faq.html')
def search_posts(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(titulo__icontains=query) if query else Post.objects.none()
    return render(request, 'Spa/search_results.html', {'posts': posts, 'query': query})
