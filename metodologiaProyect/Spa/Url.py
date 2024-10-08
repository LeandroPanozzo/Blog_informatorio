#Las rutas determinan qué vista se debe ejecutar para cada URL.
from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, RemoveImageView, UserPostListView, add_comment, delete_comment, eliminar_denuncia, eliminar_usuario, faq_view, gestionar_denuncias, mis_posts, post_delete, post_detail, resolver_denuncia, search_posts, user_posts, view_denuncias
from . import views

urlpatterns = [
    #Esta ruta vincula la URL raíz ('') con la vista home. El nombre Inicio-Spa es un identificador que puede 
    # usarse en las plantillas para generar enlaces de manera dinámica.
    path('', PostListView.as_view(), name='Inicio-Spa'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='About-Spa'),
    path('denuncias/', gestionar_denuncias, name='gestionar-denuncias'),
    path('denuncias/resolver/<int:pk>/', resolver_denuncia, name='resolver-denuncia'),
    path('post/<int:pk>/denuncia/', views.crear_denuncia, name='crear-denuncia'),
    path('post/<int:pk>/delete/', post_delete, name='post-delete'),  # Agrega esta línea
    path('denuncias/', view_denuncias, name='view-denuncias'),  # Agrega esta línea
    path('denuncias/resolver/<int:pk>/', resolver_denuncia, name='resolver-denuncia'),  # Asegúrate de tener esta línea
    path('denuncias/eliminar/<int:pk>/', eliminar_denuncia, name='denuncia-delete'),
    path('usuario/eliminar/<int:pk>/', eliminar_usuario, name='user-delete'),  # URL para eliminar usuario
     path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/remove-image/', RemoveImageView.as_view(), name='remove-image'),
    path('post/<int:post_id>/comment/', add_comment, name='add-comment'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('mis-posts/', user_posts, name='user-posts'),
    path('mis-posts/', mis_posts, name='mis-posts'),  # Asegúrate de que esto esté presente
    path('faq/', faq_view, name='faq'),
    path('search/', search_posts, name='search-posts'),
    path('post/<int:post_id>/add_comment/', add_comment, name='add-comment'),
    path('post/<int:post_id>/', post_detail, name='post-detail'),
    path('comment/delete/<int:comment_id>/', delete_comment, name='delete-comment'),
]