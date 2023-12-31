
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from LITRevu.models import Ticket, Review
from django.contrib import messages
from itertools import chain
from authentication.models import User
from authentication.forms import FollowUsersForm
from django.db import IntegrityError
from . import forms, models

@login_required
def ticket_form(request):
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
    context = {
        'ticket_form': ticket_form
    }
    return render(request, 'LITRevu/create_ticket.html', context=context)

@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(request, 'LITRevu/view_ticket.html', {'ticket': ticket})

@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    delete_form = forms.DeleteTicketForm()
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        if 'delete_ticket' in request.POST:
            delete_form = forms.DeleteTicketForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('home')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'LITRevu/edit_ticket.html', context=context)

@login_required
def review_form(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([review_form.is_valid(), ticket_form.is_valid()]):
            review = review_form.save(commit=False)
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            review.user = request.user
            ticket.save()
            review.ticket = ticket
            review.save()
    context = {
        'review_form': review_form,
        'ticket_form': ticket_form,
    }
    return render(request, 'LITRevu/create_review.html', context=context)

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    edit_form = forms.TicketForm(instance=review)
    delete_form = forms.DeleteReviewForm()
    if request.method == 'POST':
        if 'edit_review' in request.POST:
            edit_form = forms.TicketForm(request.POST, instance=review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        if 'delete_review' in request.POST:
            delete_form = forms.DeleteReviewForm(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect('home')
    context = {
        'ticket': review.ticket,
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'LITRevu/edit_review.html', context=context)

@login_required
def all_posts(request):
    current_user = request.user
    tickets = Ticket.objects.filter(user=current_user)
    reviews = Review.objects.filter(user=current_user)
    tickets_and_reviews = sorted(chain(tickets, reviews), key=lambda instance:instance.time_created, reverse=True)
    context = {
        'tickets_and_reviews': tickets_and_reviews
        }
    
    return render(request, "LITRevu/posts.html", context=context)

@login_required
def home(request):
    current_user = request.user
    tickets = Ticket.objects.filter(user=current_user)
    reviews = Review.objects.filter(user=current_user)
    tickets_and_reviews = sorted(chain(tickets, reviews), key=lambda instance:instance.time_created, reverse=True)
    context = {
        'tickets_and_reviews': tickets_and_reviews
        }
    
    return render(request, "LITRevu/home.html", context=context)

@login_required
def subscribe(request):
    form = FollowUsersForm()
    
    if request.method == 'POST':
        form = FollowUsersForm(request.POST)
    
    #     if form.is_valid():
    #         try:
    #             followed_user = User.objects.get(username=request.POST['followed_user'])
    #             if request.user == followed_user:
    #                 messages.error(request, 'Vous ne pouvez pas vous abonner à vous-même!')
    #             else:
    #                 try:
    #                     UserFollows.objects.create(user=request.user, followed_user=followed_user)
    #                     request.user.follows.add(followed_user)
    #                     messages.success(request, f'Vous êtes maintenant abonné à {followed_user}!')
    #                 except IntegrityError:
    #                     messages.error(request, f'Vous êtes déjà abonné à {followed_user}!')

    #         except User.DoesNotExist:
    #             messages.error(request, f'L\'utilisateur {form.data["followed_user"]} n\'existe pas!')
                
    # user_follows = request.user.follows.all()
    # followed_by = UserFollows.objects.filter(followed_user=request.user).order_by('user')

    context = {
        'form': form,
        # 'followed_users': user_follows,
        # 'following_users': followed_by,
    }
    return render(request, 'LITRevu/subscribe.html', context=context)