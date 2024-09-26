from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=8, required=True, label='Número de teléfono')
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=True,
        label='Dirección'
    )
    delivery_instructions = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label='Instrucciones de entrega',
        help_text='Ej: En la avenida principal, segundo callejón, ingresando por la tienda el porvenir, la casa verde, en el segundo timbre.'
    )
    contact_person_phone = forms.CharField(
        max_length=8,
        required=True,
        label='Teléfono de persona de contacto',
        help_text='Si por alguna eventualidad no puedes recibir el paquete, ¿A quién podemos llamar para que pueda recibirlo?'
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number", "address",
                  "delivery_instructions", "contact_person_phone", "password1", "password2")
        labels = {
            'username': 'Nombre de usuario',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit() or len(phone_number) != 8:
            raise ValidationError(
                "El número de teléfono debe contener 8 dígitos.")
        return phone_number

    def clean_contact_person_phone(self):
        contact_person_phone = self.cleaned_data.get('contact_person_phone')
        if not contact_person_phone.isdigit() or len(contact_person_phone) != 8:
            raise ValidationError(
                "El número de teléfono de contacto debe contener 8 dígitos.")
        return contact_person_phone


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}), label='Nombre de usuario')
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Contraseña'}), label='Contraseña')


class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Correo electrónico')
    phone_number = forms.CharField(
        max_length=8, required=True, label='Número de teléfono')
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=True,
        label='Dirección'
    )
    delivery_instructions = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label='Instrucciones de entrega',
        help_text='Ej: En la avenida principal, segundo callejón, ingresando por la tienda el porvenir, la casa verde, en el segundo timbre.'
    )
    contact_person_phone = forms.CharField(
        max_length=8,
        required=True,
        label='Teléfono de persona de contacto',
        help_text='Si por alguna eventualidad no puedes recibir el paquete, ¿A quién podemos llamar para que pueda recibirlo?'
    )

    class Meta:
        model = CustomUser
        fields = ("email", "phone_number", "address",
                  "delivery_instructions", "contact_person_phone")
