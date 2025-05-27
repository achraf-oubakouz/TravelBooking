from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from projet import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('voyages/', views.voyage_list, name='voyage_list'),
    path('voyage/<int:voyage_id>/', views.voyage_detail, name='voyage_detail'),
    path('reservation/create/<int:voyage_id>/', views.reservation_create, name='reservation_create'),
    path('confirmation/<int:reservation_id>/', views.confirmation, name='confirmation'),
    path('reservation/<int:reservation_id>/pdf/', views.reservation_pdf, name='reservation_pdf'),
    path('reservation/<int:reservation_id>/cancel/', views.annuler_reservation, name='cancel_reservation'),
    path('payment/<int:reservation_id>/', views.payment, name='payment'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
