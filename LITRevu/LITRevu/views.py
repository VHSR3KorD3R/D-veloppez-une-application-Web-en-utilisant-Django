
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from . import forms

@login_required
def home(request):
    return render(request, 'LITRevu/home.html')

@login_required
def ticket_creation_form(request):
    ticket_creation_form = forms.TicketCreationForm()
    if request.method == 'POST':
        ticket_creation_form = forms.TicketCreationForm(request.POST)
        if ticket_creation_form.is_valid():
            ticket = ticket_creation_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
    context = {
        'ticket_creation_form': ticket_creation_form
    }
    return render(request, 'LITRevu/create_ticket.html', context=context)
