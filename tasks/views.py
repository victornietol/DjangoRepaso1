from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # Manejo de registro y autenticacion de usuarios
from django.contrib.auth.models import User
from django.contrib.auth import login, logout # Manejo de cookies para inicios de seison
from django.db import IntegrityError

# Create your views here.
def home(request):
    return render(request, 'home.html')

def tasks(request):
    return render(request, 'tasks.html')

def signup(request):
    # Validar si es GET para mostrar la interfaz, o si es POST para recibir datos
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': None
        })
    else: 
        # Registrar al nuevo usuario
        # Validar que las nuevas contraseñas coincidan
        if request.POST['password1'] == request.POST['password2']:
            # Se intenta registrar al usuario
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save() # Guardar el usuario en la BD
                print("Se registro")
                login(request, user) # Generar cookie de inicio de sesion con el usuario
                return redirect("tasks")

            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': "El usuario ya existe."
                })
            except Exception as e:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': f"{e}"
                })
            
        else:
            print("No se registro")
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': "Las contraseñas no conciden"
            })
        
def cerrar_sesion(request):
    logout(request)
    return redirect('home')