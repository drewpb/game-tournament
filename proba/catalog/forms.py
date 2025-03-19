from django import forms
from .models import Torneo, Usuario
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class AdminActionForm(forms.Form):
    ACTION_CHOICES = [
        ('generate_users', 'Generar Usuarios'),
        ('view_statistics', 'Ver Estadísticas'),
        ('manage_tournaments', 'Gestionar Torneos')
    ]

    action = forms.ChoiceField(choices=ACTION_CHOICES, label='Seleccione la acción')

class TorneoForm(forms.ModelForm):
    class Meta:
        model = Torneo
        fields = ['nombre', 'videojuego', 'clasif_sistem', 'reglas', 'fecha_inicio', 'fecha_fin', 'n_participantes',
                  'premio']

        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        # Validación adicional: La fecha de fin debe ser posterior a la fecha de inicio
        if fecha_inicio and fecha_fin and fecha_fin <= fecha_inicio:
            raise forms.ValidationError("La fecha de fin debe ser posterior a la fecha de inicio.")

        return cleaned_data

class JugadorRegistroForm(UserCreationForm):
    # Agregar los campos que necesitas además de los que ya existen en AbstractBaseUser
    nombre = forms.CharField(max_length=100, help_text='Nombre y Apellidos del usuario',
                             widget=forms.TextInput(attrs={'autofocus': ''}))
    email = forms.EmailField(help_text='Introduce tu email')
    dni = forms.CharField(max_length=20, help_text='DNI')
    telefono = forms.CharField(max_length=15, help_text='Teléfono')
    alias = forms.CharField(max_length=50, help_text='Alias visible en el juego')

    class Meta:
        model = Usuario  # Si es para registrar jugadores, puedes usar Jugador
        fields = ['nombre', 'email', 'dni', 'telefono', 'alias', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Alias", max_length=150, widget=forms.TextInput(attrs={'autofocus': ''}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
