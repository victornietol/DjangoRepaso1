'''
    Crear formulario personalizado segun el modelo de la tabla creada en la base datos.
    En este formulario se incluyen los campos ya definidos previamente.
'''

from django.forms import ModelForm
from .models import Task

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['titulo','descripcion','importante']