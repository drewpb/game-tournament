from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm  # Para el logeo
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate  # logout: Para salir

from .models import Torneo, Usuario, Videojuego, Participacion, Partida, Resultado
from .forms import TorneoForm, JugadorRegistroForm, UserLoginForm # Formulario para crear torneos y registro de jugadores
##########################################################################
from .forms import AdminActionForm # Creado en forms para gestion Admin en web
from django.contrib.auth.decorators import user_passes_test


# Función para verificar si el usuario es un administrador
def is_admin(user):
    return hasattr(user, 'admin')  # Solo los usuarios que tienen el atributo 'admin'

# Vista para el panel de administración
@user_passes_test(is_admin)
def admin_panel(request):
    if request.method == 'POST':
        form = AdminActionForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data['action']
            # Redireccionar según la acción seleccionada
            if action == 'generate_users':
                return redirect('generate_users')
            elif action == 'view_statistics':
                return redirect('view_statistics')
            elif action == 'manage_tournaments':
                return redirect('manage_tournaments')
    else:
        form = AdminActionForm()

    return render(request, 'admin_panel.html', {'form': form})

# Vista para generar usuarios
@user_passes_test(is_admin)
def generate_users(request):
    if request.method == 'POST':
        # Aquí puedes insertar el código de generación de usuarios usando Faker
        # Reutiliza el código que probaste en el shell
        pass  # Implementar lógica aquí

    return render(request, 'generate_users.html')

# Vista para ver estadísticas
@user_passes_test(is_admin)
def view_statistics(request):
    jugadores = Usuario.objects.all()
    return render(request, 'view_statistics.html', {'jugadores': jugadores})

# Vista para gestionar torneos
@user_passes_test(is_admin)
def manage_tournaments(request):
    # Aquí puedes agregar la lógica para gestionar torneos
    pass  # Implementar lógica aquí

##########################################################################

def index(request):
    torneos = Torneo.objects.all().order_by('-fecha_inicio')[:6]  # Muestra los 6 torneos más recientes
    videojuegos = Videojuego.objects.all()
    print(Usuario.alias)
    context = {'torneos': torneos, 'videojuegos': videojuegos}
    return render(request, 'index.html', context)

@login_required
def profile_view(request):
    nombre = Usuario.nombre
    dni = Usuario.dni
    print(Usuario.alias)
    context = {'nombre': nombre, 'dni': dni}
    return render(request, 'registration/profile.html')

def custom_logout_view(request):
    logout(request)
    return redirect('index')  # O la página a la que quieras redirigir

def registro(request):
    if request.method == 'POST':
        form = JugadorRegistroForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda el jugador
            # Iniciar sesión automáticamente después del registro
            login(request, user)
            return redirect('index')  # O la página a la que quieras redirigir
    else:
        form = JugadorRegistroForm()
    return render(request, 'registration/register.html', {'form': form})

def logeo(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        print(" >>> Flag__Logeo")
        if form.is_valid():
            print("Form is VALID!!")
            # Autenticamos al usuario usando 'alias' como 'username'
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            print(username, password)
            if user is not None:
                print(user)
                login(request, user)
                return redirect('index')  # Redirige a la página de inicio u otra página
            else:
                # Mensaje de error si las credenciales no son válidas
                form.add_error(None, "Alias o contraseña incorrectos.")
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')  # Redirigir a la página de inicio de sesión después del registro


# Listado de Torneos
class TorneoListView(ListView):
    model = Torneo
    template_name = 'torneos/torneo_list.html'  # Plantilla a usar
    context_object_name = 'torneos'

# Detalle de un Torneo
class TorneoDetailView(DetailView):
    model = Torneo
    template_name = 'torneos/torneo_detail.html'
    context_object_name = 'torneo'

# Crear un Torneo (Solo Administradores)
class TorneoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Torneo
    form_class = TorneoForm
    template_name = 'torneos/torneo_form.html'
    success_url = reverse_lazy('torneo-list')

    def test_func(self):
        # Solo los administradores pueden crear torneos
        return self.request.user.is_authenticated and hasattr(self.request.user, 'admin')

    def form_valid(self, form):
        form.instance.administrador = self.request.user.admin  # Asigna el administrador actual
        return super().form_valid(form)

# Registro en un Torneo (jugador se inscribe en un torneo)
class TorneoRegisterView(LoginRequiredMixin, View):
    def post(self, request, pk):
        torneo = get_object_or_404(Torneo, pk=pk)
        jugador = request.user.jugador  # Suponiendo que el usuario está registrado como jugador
        if torneo.jugadores.count() < torneo.n_participantes:
            torneo.jugadores.add(jugador)
            torneo.save()
            return redirect('torneo-detail', pk=pk)
        return redirect('torneo-list')  # Si el torneo ya está lleno, redirigimos al listado

# Listado de Jugadores
class JugadorListView(ListView):
    model = Usuario
    template_name = 'jugadores/jugador_list.html'
    context_object_name = 'jugadores'

# Detalle de un Jugador
class JugadorDetailView(DetailView):
    model = Usuario
    template_name = 'jugadores/jugador_detail.html'
    context_object_name = 'jugador'

# Listado de Resultados
class ResultadoListView(ListView):
    model = Resultado
    template_name = 'resultados/resultado_list.html'
    context_object_name = 'resultados'

# Detalle de un Resultado
class ResultadoDetailView(DetailView):
    model = Resultado
    template_name = 'resultados/resultado_detail.html'
    context_object_name = 'resultado'
