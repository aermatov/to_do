from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'is_private']  # Убрали 'user' и 'is_completed'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Настраиваем виджеты
        self.fields['description'].widget = forms.Textarea(
            attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Описание задачи (необязательно)'
            }
        )
        self.fields['title'].widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Название задачи'
            }
        )
        self.fields['is_private'].widget = forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
            }
        )

        # Делаем описание необязательным
        self.fields['description'].required = False
