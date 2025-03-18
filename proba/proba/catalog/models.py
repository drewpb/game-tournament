from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid  # Para generar identificadores únicos


# Manager personalizado para el modelo Usuario
class UsuarioManager(BaseUserManager):
    def create_user(self, alias, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(alias=alias, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, alias, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superusuario debe tener is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superusuario debe tener is_superuser=True.")

        return self.create_user(alias, email, password, **extra_fields)


# Modelo de usuario principal
class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=100, help_text='Nombre completo del usuario')
    email = models.EmailField(unique=True, help_text='Correo electrónico único')
    dni = models.CharField(max_length=20, unique=True, help_text='Documento de identidad único')
    telefono = models.CharField(max_length=15, blank=True, help_text='Número de teléfono')
    alias = models.CharField(max_length=50, unique=True, help_text='Alias visible para otros usuarios')

    # Campos de permisos y roles
    is_active = models.BooleanField(default=True, help_text='Determina si el usuario está activo')
    is_staff = models.BooleanField(default=False, help_text='Determina si el usuario puede acceder al admin')
    is_superuser = models.BooleanField(default=False, help_text='Determina si el usuario es superusuario')

    # Campos adicionales
    estadisticas = models.JSONField(null=True, blank=True, help_text='Estadísticas generales del usuario')
    partidas_ganadas_totales = models.IntegerField(default=0, help_text='Número total de partidas ganadas')
    puntos_totales = models.IntegerField(default=0, help_text='Puntos totales acumulados')

    # Campos requeridos por Django para el modelo de usuario
    USERNAME_FIELD = 'alias'
    REQUIRED_FIELDS = ['nombre', 'email', 'dni']

    objects = UsuarioManager()

    def __str__(self):
        return self.alias


# Modelo para videojuegos
class Videojuego(models.Model):
    nombre = models.CharField(max_length=100, unique=True, help_text='Nombre del videojuego')
    imagen = models.ImageField(upload_to='videojuegos/', blank=True, null=True, help_text='Imagen del videojuego')

    def __str__(self):
        return self.nombre


# Modelo para torneos
class Torneo(models.Model):
    nombre = models.CharField(max_length=100, help_text='Nombre del torneo')
    codigo = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    videojuego = models.ForeignKey(Videojuego, on_delete=models.CASCADE, help_text='Videojuego asociado al torneo')
    clasif_sistem = models.CharField(max_length=100, help_text='Sistema de clasificación (puntos, eliminatoria, etc.)')
    reglas = models.TextField(help_text='Reglas del torneo')
    fecha_inicio = models.DateField(help_text='Fecha de inicio del torneo')
    fecha_fin = models.DateField(help_text='Fecha de finalización del torneo')
    estado = models.CharField(
        max_length=20,
        choices=[('p', 'Pendiente'), ('c', 'En curso'), ('f', 'Finalizado'), ('canc', 'Cancelado')],
        default='p',
        help_text='Estado actual del torneo'
    )
    jugadores = models.ManyToManyField(Usuario, related_name='torneos', blank=True)
    n_participantes = models.PositiveIntegerField(help_text='Número de participantes requerido para comenzar')
    premio = models.JSONField(help_text='Premios del torneo (ejemplo: {"1°": "Premio 1"})')
    ganadores = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='torneos_ganados')

    def inscribir_jugador(self, jugador):
        if self.jugadores.count() < self.n_participantes:
            self.jugadores.add(jugador)
            if self.jugadores.count() == self.n_participantes:
                self.estado = 'c'  # Cambia a "En curso" cuando se completan los cupos
            self.save()
        else:
            raise ValueError("El torneo ya tiene el número máximo de participantes.")

    def __str__(self):
        return self.nombre


# Modelo para partidas dentro de un torneo
class Partida(models.Model):
    nombre = models.CharField(max_length=100, help_text='Nombre de la partida')
    fecha_hora = models.DateTimeField(help_text='Fecha y hora de la partida')
    videojuego = models.ForeignKey(Videojuego, on_delete=models.CASCADE)
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name='partidas')

    def __str__(self):
        return self.nombre


# Modelo intermedio para registrar participación de jugadores
class Participacion(models.Model):
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, related_name='participaciones')
    jugador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    puntaje = models.IntegerField(default=0, help_text='Puntaje del jugador en la partida')
    resultado = models.CharField(max_length=100, blank=True, help_text='Resultado (ganador, perdedor, empate, etc.)')
    tiempo_jugado = models.DurationField(null=True, blank=True, help_text='Duración de la participación')
    otras_estadisticas = models.JSONField(null=True, blank=True, help_text='Otras estadísticas del jugador')

    def __str__(self):
        return f"{self.jugador.alias} - {self.partida.nombre}"


# Modelo para resultados específicos
class Resultado(models.Model):
    participacion = models.ForeignKey(Participacion, on_delete=models.CASCADE, related_name='resultados')
    descripcion = models.CharField(max_length=100, help_text='Descripción del resultado')
    puntaje = models.IntegerField(help_text='Puntaje final del jugador')
    otras_estadisticas = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Resultado de {self.participacion.jugador.alias} en {self.participacion.partida.nombre}"


# Modelo para estadísticas específicas por videojuego
class EstadisticasVideojuego(models.Model):
    jugador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='estadisticas_videojuego')
    videojuego = models.CharField(max_length=100, help_text='Nombre del videojuego')
    partidas_ganadas = models.IntegerField(default=0)
    partidas_perdidas = models.IntegerField(default=0)
    puntos = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.jugador.alias} - {self.videojuego}"
