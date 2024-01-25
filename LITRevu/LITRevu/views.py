
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from LITRevu.models import Ticket, Review
from django.contrib import messages
from itertools import chain
from authentication.models import User
from authentication.forms import FollowUsersForm
from django.db import IntegrityError
from . import forms, models
from django.views.generic import DeleteView

@login_required
def ticket_form(request):
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            print("gidfidfy")
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("home")
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
    if request.method == 'POST':
        edit_form = forms.TicketForm(request.POST, instance=ticket)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('posts')
    context = {
        'edit_form': edit_form,
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
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    context = {
        'ticket': ticket
        }    
    
    if request.method == 'GET':
        return render(request, 'LITRevu/post_confirm_delete.html',context)
    elif request.method == 'POST':
        ticket.delete()
        return redirect('posts')

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review_form = forms.ReviewForm(instance=review)
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.save()
            return redirect('posts')
    context = {
        'ticket': review.ticket,
        'review_form': review_form,
    }
    return render(request, 'LITRevu/edit_review.html', context=context)

@login_required
def delete_review(request, review_id):
    # review = Review.objects.get(id=review_id)
    # if request.user == review.user:
    #     print('test')
    #     if request.method == 'POST':
    #         print('deleted')
    #         review.delete()
    # return redirect('posts')
    #return render(request, 'LITRevu/delete_review.html', {'review': review})
    review = get_object_or_404(Review, id=review_id)
    context = {
        'review': review
        }    
    
    if request.method == 'GET':
        return render(request, 'LITRevu/post_confirm_delete.html',context)
    elif request.method == 'POST':
        review.delete()
        return redirect('posts')

def create_review_with_ticket(request, ticket_id):
    print(type(ticket_id))
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    review_form = forms.ReviewForm()

    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('posts')
    
    context = {
        'review_form': review_form,
        'ticket': ticket,
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
    tickets_followed = Ticket.objects.filter(user__in=current_user.follows.all())
    reviews_followed = Review.objects.filter(user__in=current_user.follows.all())
    print(tickets_followed)
    print(reviews_followed)
    
    for ticket in tickets_followed:
        ticket.has_review = Review.objects.filter(ticket=ticket).exists()
        print(ticket.has_review)
        print(type(ticket))
        
    tickets_and_reviews = sorted(chain(tickets, reviews, tickets_followed, reviews_followed), key=lambda instance:instance.time_created, reverse=True)
    context = {
        'tickets_and_reviews': tickets_and_reviews
        }
    
    
    return render(request, "LITRevu/home.html", context=context)

@login_required
def subscribe(request):
    form = FollowUsersForm()
    
    if request.method == 'POST':
        form = FollowUsersForm(request.POST)
    
        if form.is_valid():
            try:
                followed_user = User.objects.get(username=request.POST['followed_user'])
                if request.user == followed_user:
                    messages.error(request, 'Vous ne pouvez pas vous abonner à vous-même!')
                else:
                    try:
                        request.user.follows.add(followed_user)
                        messages.success(request, f'Vous êtes maintenant abonné à {followed_user}!')
                    except IntegrityError:
                        messages.error(request, f'Vous êtes déjà abonné à {followed_user}!')

            except User.DoesNotExist:
                messages.error(request, f'L\'utilisateur {form.data["followed_user"]} n\'existe pas!')
                
    user_follows = request.user.follows.all()
    followed_by = User.objects.filter(follows=request.user)
    print(followed_by)

    context = {
        'form': form,
        'followed_users': user_follows,
        'following_users': followed_by,
    }
    return render(request, 'LITRevu/subscribe.html', context=context)

@login_required
def unsubscribe(request, user_id):
    user = get_object_or_404(User, id=user_id)
    request.user.follows.remove(user)
    
    return redirect('subscribe')