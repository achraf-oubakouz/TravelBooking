from django.db import models
from django.contrib.auth.models import User

class Voyage(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    destination = models.CharField(max_length=100)
    prix_base = models.DecimalField(max_digits=8, decimal_places=2)
    duree = models.IntegerField(help_text="Durée en jours")
    date_depart = models.DateField()
    photo = models.ImageField(upload_to='voyages/', blank=True, null=True)

    def __str__(self):
        return self.titre
    
class Option(models.Model):
    voyage = models.ForeignKey(Voyage, related_name="options", on_delete=models.CASCADE)
    nom = models.CharField(max_length=255)
    description = models.TextField() 
    prix = models.DecimalField(max_digits=10, decimal_places=2)  
    def __str__(self):
        return self.nom

class Reservation(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE)
    date_reservation = models.DateTimeField(auto_now_add=True)
    nombre_personnes = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Réservation #{self.id} par {self.utilisateur.username}"

class Paiement(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='paiement')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=50, choices=[('en_attente', 'En attente'), ('effectué', 'Effectué')])

    def __str__(self):
        return f"Paiement de {self.montant} DH pour {self.reservation}"
