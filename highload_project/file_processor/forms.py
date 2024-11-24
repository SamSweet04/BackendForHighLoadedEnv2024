from django import forms

class FileUploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        if not uploaded_file.name.endswith('.csv'):
            raise forms.ValidationError("Only CSV files are allowed.")
        return uploaded_file
