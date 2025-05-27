from django.shortcuts import render, get_object_or_404, redirect
from .models import Paiement, Voyage, Reservation
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import ReservationForm, PaymentForm
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa




def home(request):
    voyages = Voyage.objects.all()[:6]
    return render(request, 'home.html', {'voyages': voyages})

def voyage_list(request):
    voyages = Voyage.objects.all()
    query = request.GET.get('q', '')
    destination = request.GET.get('destination', '')
    duree_min = request.GET.get('duree_min')
    duree_max = request.GET.get('duree_max')
    prix_min = request.GET.get('prix_min')
    prix_max = request.GET.get('prix_max')

    if query:
        voyages = voyages.filter(titre__icontains=query)
    if destination:
        voyages = voyages.filter(destination=destination)
    if duree_min:
        voyages = voyages.filter(duree__gte=duree_min)
    if duree_max:
        voyages = voyages.filter(duree__lte=duree_max)
    if prix_min:
        voyages = voyages.filter(prix_base__gte=prix_min)
    if prix_max:
        voyages = voyages.filter(prix_base__lte=prix_max)

    destinations = Voyage.objects.values_list('destination', flat=True).distinct()

    context = {
        'voyages': voyages,
        'query': query,
        'duree_min': duree_min or '',
        'duree_max': duree_max or '',
        'prix_min': prix_min or '',
        'prix_max': prix_max or '',
        'destinations': destinations,
    }

    return render(request, 'voyage_list.html', context)


def voyage_detail(request, voyage_id):
    voyage = get_object_or_404(Voyage, id=voyage_id)
    return render(request, 'voyage_detail.html', {'voyage': voyage})



@login_required
def confirmation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, utilisateur=request.user)
    return render(request, 'confirmation.html', {'reservation': reservation})

@login_required
def annuler_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, utilisateur=request.user)
    if request.method == 'POST':
        reservation.delete()
        return redirect('profile')
    return render(request, 'cancel_confirmation.html', {'reservation': reservation})

@login_required
def profile(request):
    reservations = Reservation.objects.filter(utilisateur=request.user)
    return render(request, 'profile.html', {'reservations': reservations})

@login_required
def dashboard(request):
    total_voyages = Voyage.objects.count()
    total_reservations = Reservation.objects.count()
    paiements_en_attente = Paiement.objects.filter(statut='en_attente').count()
    chiffre_affaires = Paiement.objects.filter(statut='effectué').aggregate(total=Sum('montant'))['total'] or 0

    context = {
        'total_voyages': total_voyages,
        'total_reservations': total_reservations,
        'chiffre_affaires': chiffre_affaires,
        'paiements_en_attente': paiements_en_attente,
    }
    return render(request, 'dashboard.html', context)


def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            return redirect('login')
    else:
        user_form = UserCreationForm()
    return render(request, 'register.html', {'user_form': user_form})


@login_required
def reservation_create(request, voyage_id):
    voyage = get_object_or_404(Voyage, id=voyage_id)
    options = [
        {
            'id': option.id,
            'name': option.nom,
            'price': option.prix
        }
    
        for option in voyage.options.all() 
    ]

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.utilisateur = request.user
            reservation.voyage = voyage
            reservation.total = voyage.prix_base * reservation.nombre_personnes
            reservation.save()
        
            return redirect('payment', reservation_id=reservation.id)
    else:
        form = ReservationForm()
    return render(request, 'reservation.html', {'form': form, 'voyage': voyage, 'options': options})


@login_required
def reservation_pdf(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, utilisateur=request.user)
    html_string = render_to_string('confirmation_pdf.html', {'reservation': reservation})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="confirmation_{reservation.id}.pdf"'
    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    return response

@login_required
def payment(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, utilisateur=request.user)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():

            paiement = Paiement(
                reservation=reservation,
                montant=reservation.total,
                statut='effectué' 
            )
            paiement.save()
           
            return redirect('confirmation', reservation_id=reservation.id)
    else:
        form = PaymentForm()
    return render(request, 'payment.html', {'form': form, 'reservation': reservation})