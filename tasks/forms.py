'''
    Crear formulario personalizado segun el modelo de la tabla creada en la base datos.
    En este formulario se incluyen los campos ya definidos previamente.
'''

from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['titulo','descripcion','importante']
        # En widgets se indican las etiquetas o campos que se van a estilizar para el formulario
        widgets = {
            # Se indica la etique, despues se utiliza 'forms' y se indican lo elementos y los atributos, en este diccionario se indica el parametro y su valor, en este caso 'class' : 'lo que va a llevar la clase'
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Ingresa un titulo"
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Ingresa una descripcion"
            }),
            'importante': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }