from django.urls import path
from .views import index, profile_view, logeo, registro, TorneoListView, TorneoDetailView, TorneoCreateView, TorneoRegisterView, JugadorListView, JugadorDetailView
from . import views

# Para las imagenes:
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),  # Página de inicio
    path('login/', logeo, name='login'),
    path('accounts/logout/', views.custom_logout_view, name='logout'),
    path('register/', registro, name='register'),  # Vista para el registro
    path('accounts/profile/', profile_view, name='profile'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),

    path('torneos/', TorneoListView.as_view(), name='torneo_list'),
    path('torneos/<int:pk>/', TorneoDetailView.as_view(), name='torneo_detail'),
    path('torneos/<int:pk>/register/', TorneoRegisterView.as_view(), name='torneo_register'),
    path('torneos/nuevo/', TorneoCreateView.as_view(), name='torneo_create'),
    path('jugadores/', JugadorListView.as_view(), name='jugador_list'),
    path('jugadores/<int:pk>/', JugadorDetailView.as_view(), name='jugador_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
