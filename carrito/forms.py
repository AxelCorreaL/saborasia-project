# Importa UserCreationForm de django.contrib.auth.forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

# Crea un formulario personalizado de creación de usuarios que utilice el campo de correo electrónico
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # Especifica el modelo de usuario personalizado y el campo de correo electrónico como el único campo requerido
        model = CustomUser
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cambia las etiquetas de los campos si lo deseas
        self.fields['email'].label = 'Correo electrónico'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def save(self, commit=True):
        # Guarda el usuario utilizando el campo de correo electrónico
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
