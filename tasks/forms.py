from django import forms
from django.utils import timezone
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'is_private', 'description', 'is_completed', 'user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the user field optional in the form
        self.fields['user'].required = False
        # Customize the is_completed field to be more user-friendly
        self.fields['is_completed'].widget = forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }
        )
        self.fields['description'].widget = forms.Textarea(attrs={'rows': 4})

    def clean_is_completed(self):
        is_completed = self.cleaned_data.get('is_completed')
        # If the task is being marked as completed but no date was provided,
        # automatically set it to now
        if is_completed and not self.cleaned_data['is_completed']:
            return timezone.now()
        return is_completed