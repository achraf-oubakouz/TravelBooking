from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['nombre_personnes']
        widgets = {
            'nombre_personnes': forms.NumberInput(attrs={'class': 'form-control', 'min': 1})
        }


class PaymentForm(forms.Form):
    mode = forms.ChoiceField(
        choices=[('carte', 'Carte bancaire'), ('paypal', 'PayPal'), ('virement', 'Virement bancaire')],
        widget=forms.Select(attrs={'class': 'form-control'})
        
    )