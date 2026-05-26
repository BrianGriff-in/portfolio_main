from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework import generics
from .models import ContactMessage
from .forms import ContactForm
from .serializers import ContactMessageSerializer
from home.models import HeroSection  # add this

def contact(request):
    hero = HeroSection.objects.first()  # add this
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('contact:contact')
    else:
        form = ContactForm()
    return render(request, 'contact/contact.html', {'form': form, 'hero': hero})

class ContactMessageListAPI(generics.ListAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

class ContactMessageCreateAPI(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer