from django import forms
from .models import Project, ProjectImage, Category

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['category', 'title', 'slug']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do projeto'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'id': 'slug-input'}),
        }

# Isso replica o "ProjectImageInline" do seu admin.py
ProjectImageFormSet = forms.inlineformset_factory(
    Project, 
    ProjectImage, 
    fields=['image'], 
    extra=1,  # Começa apenas com um campo
    can_delete=True
)