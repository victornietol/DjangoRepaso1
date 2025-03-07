from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # Manejo de registro y autenticacion de usuarios
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate # Manejo de cookies para inicios de seison
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required # Verificar que el usuario este logueado para poder acceder a ciertas rutas (es un decorador)

# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required
def tasks(request):
    tareas = Task.objects.filter(user=request.user, fecha_completada=None) # Devuelve las tareas de la BD del usuario logeado, se pueden agregar mas criterios de busqueda
    return render(request, 'tasks.html', {
        'tasks': tareas
    })

@login_required
def create_task(request):
    # Verificar que se haya iniciado sesion con un usuario
    if 'sessionid' not in request.COOKIES: # No se inicio sesion, (esta condicional se omite si se coloca el decorador 'login_required', ya que realiza esta comprobacion automaticamnte, pero la dejo por motivos de practicar cosas)
        return redirect('login')
    else: # Si se inicio sesion
        if request.method == 'GET':
            # Solo se cargo la pagina
            return render(request, 'create_task.html', {
                'form':TaskForm
            })
        else:
            # Se reciben los datos del formulario
            try:
                form = TaskForm(request.POST)
                nueva_tarea = form.save(commit=False) # Obtener datos de la nueva tarea
                nueva_tarea.user = request.user # Agregando usuario
                nueva_tarea.save() # Guardar tarea
                return redirect('tasks')
            except ValueError:
                return render(request, 'create_task.html', {
                    'form':TaskForm,
                    'mensaje': f"Error: Valor incorrecto introducido"
                })
            except Exception as e:
                return render(request, 'create_task.html', {
                    'form':TaskForm,
                    'mensaje': f"Error: {e}"
                })

@login_required
def task_detail(request, tarea_id): # el parametro debe llamarse igual que en urls.py
    if request.method == "GET":
        tarea = get_object_or_404(Task, pk=tarea_id, user=request.user) # Obtener tarea y solo muestra las del usuario logueado
        form = TaskForm(instance=tarea)
        return render(request, 'task_detail.html', {
            'tarea': tarea,
            'form': form
        })
    else:
        try:
            tarea = get_object_or_404(Task, pk=tarea_id, user=request.user)
            form = TaskForm(request.POST, instance=tarea) # Actualizando formulario
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'tarea': tarea,
                'form': form,
                'error': f"Error al actualizar, valor incorrecto."
                })
        except Exception as e:
            return render(request, 'task_detail.html', {
                'tarea': tarea,
                'form': form,
                'error': f"Error al actualizar: {e}."
            })

@login_required        
def complete_task(request, tarea_id): # el parametro debe llamarse igual que en urls.py
    tarea = get_object_or_404(Task, pk=tarea_id, user=request.user)
    if request.method == 'POST':
        tarea.fecha_completada = timezone.now()
        tarea.save()
        return redirect('tasks')

@login_required 
def delete_task(request, tarea_id): # el parametro debe llamarse igual que en urls.py
    tarea = get_object_or_404(Task, pk=tarea_id, user=request.user)
    if request.method == 'POST':
        tarea.delete()
        return redirect('tasks')

@login_required
def tasks_completed(request):
    tareas = Task.objects.filter(user=request.user, fecha_completada__isnull=False).order_by('-fecha_completada')
    return render(request, 'tasks.html', {
        'tasks': tareas,
        'completadas': True
    })

def signup(request):
    if 'sessionid' not in request.COOKIES: # Si esta logueado se manda al inicio
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
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': "Las contraseñas no conciden"
                })
    else:
        return redirect('home')

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('home')

def iniciar_sesion(request):
    if 'sessionid' not in request.COOKIES:
        if request.method == 'GET':
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': None
            })
        else: 
            # Autenticar usuario
            user = authenticate(request,
                username=request.POST['username'],
                password=request.POST['password']
            )
            
            if user is None: # Si no se devuelve objeto entonces no hay usuario
                return render(request, 'login.html', {
                    'form': AuthenticationForm,
                    'error': "El usuario o la contraseña son incorrectos."
                })
            else: #  Se inicia sesion y se genera un cookie
                login(request, user)
                return redirect('tasks')
    else:
        return redirect('home')
