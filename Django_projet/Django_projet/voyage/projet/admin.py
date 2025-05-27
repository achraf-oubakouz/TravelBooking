from django.contrib import admin
from .models import Voyage
from .models import Reservation
from .models import Paiement
from .models import Option

admin.site.register(Voyage)
admin.site.register(Reservation)
admin.site.register(Paiement)
admin.site.register(Option)

