from django import forms
from .models import File

# Model form
class FileUploadModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file','original_name')

        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'original_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Este campo se rellena solo'}),
        }

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in ["csv"]:
            raise forms.ValidationError("Solo aceptamos archivos .csv")
        return file
    
    def clean_original_name(self):
        file = self.cleaned_data.get('file')
        if file != None:
            return file.name


