from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from .forms import *
from .models import *

import json


@login_required(login_url='user_management:login')
def showrooms(request):
    return render(request, "showrooms/owned-showrooms.html", {"active_tab": "showrooms"})


@login_required(login_url='user_management:login')
def list_of_showrooms(request):
    users_showrooms = Showroom.objects.filter(
        Q(owner=request.user.profile) |
        Q(showroomcollaborator__collaborator=request.user.profile, 
          showroomcollaborator__status='ACCEPTED')        
    ).distinct().order_by('-date_created')

    page = int(request.GET.get("page", 1))

    if page == 1:
        showrooms_to_display = users_showrooms[:3]  # first 3
        has_next = users_showrooms.count() > 3
        has_previous = False
        num_pages = (users_showrooms.count() - 3 + 3) // 4 + 1  # +1 for first page
    else:
        remaining_showrooms = users_showrooms[3:]
        paginator = Paginator(remaining_showrooms, 4)
        current_page = paginator.get_page(page - 1)  # shift pages down by 1
        showrooms_to_display = current_page.object_list
        has_next = current_page.has_next()
        has_previous = current_page.has_previous() or True  # always allow going back to page 1
        num_pages = paginator.num_pages + 1  # add page 1


    showroom_data = [
        {
            "id": showroom.id,
            "title": showroom.title,
            "cover_image": showroom.cover_image.url if showroom.cover_image else "",
            "slug": showroom.slug,
        }
        for showroom in showrooms_to_display
    ]

    return JsonResponse({
        "showrooms": showroom_data,
        "has_next": has_next,
        "has_previous": has_previous,
        "current_page": page,
        "num_pages": num_pages
    })


@login_required(login_url='user_management:login')
def showroom_detail(request, pk, slug=None):
    showroom = Showroom.objects.get(pk=pk)
    outfit_count = showroom.outfits.count()
    follower_count = showroom.followers.count()
    accepted_collaborators = ShowroomCollaborator.objects.filter(
        showroom=showroom,
        status='ACCEPTED'
        ).select_related('collaborator')


    is_follower = showroom.followers.filter(id=request.user.profile.id).exists()

    is_collaborator = accepted_collaborators.filter(collaborator=request.user.profile).exists()

    is_owner = showroom.owner==request.user.profile

    if slug != showroom.slug:
        return redirect('showrooms:showroom_detail', pk=pk, slug=showroom.slug)
    
    return render(request, 'showrooms/showroom-detail.html', {
        'showroom': showroom,
        'accepted_collaborators': accepted_collaborators,
        'outfit_count': outfit_count,
        'follower_count': follower_count,
        'show_follow_button': not (is_follower or is_collaborator or is_owner),
        'show_edit_button': is_owner or is_collaborator,
        'if_following': is_follower
        })


@login_required(login_url='user_management:login')
def showroom_outfits(request, pk):
    showroom = Showroom.objects.get(pk=pk)
    outfits = showroom.outfits.all()
    data = []
    for outfit in outfits:
        data.append({
        'id': outfit.id,
        'image': outfit.image.url if outfit.image else '',
    })
    return JsonResponse({'outfits': data})


@login_required(login_url='user_management:login')
def create_showroom(request):
    user_profile = request.user.profile

    if request.method == 'POST':
        form = ShowroomCreateForm(request.POST, request.FILES)
        if form.is_valid():
            showroom = form.save(commit=False)
            showroom.owner = user_profile
            showroom.save()

            # Save collaborators
            collaborators = form.cleaned_data.get('collaborators', [])
            for collab in collaborators:
                ShowroomCollaborator.objects.create(
                    showroom=showroom,
                    collaborator=collab,
                    invited_by=user_profile,
                    status='PENDING'
                )

            # Handle tags
            tags = request.POST.get("tags", "").split(",")
            showroom.tags.set(tags[:3])

            return redirect('showrooms:showroom_detail', pk=showroom.id, slug=showroom.slug)
            # Return redirect header for HTMX
            # detail_url = reverse('showrooms:showroom_detail', kwargs={
            #     'pk': showroom.id,
            #     'slug': showroom.slug
            # }) + "?just_created=1"
            # return HttpResponse(
            #     "", 
            #     headers={"HX-Redirect": detail_url}
            # )

    else:
        form = ShowroomCreateForm()

    return render(request, 'showrooms/showroom-create.html', {
        'form': form
    })
        

@login_required(login_url='user_management:login')
def create_showroom_outfit_modal(request):
    user_profile = request.user.profile
    outfits = user_profile.outfits.all()
    data = []
    for outfit in outfits:
        data.append({
        'id': outfit.id,
        'image': outfit.image.url if outfit.image else '',
    })
    return JsonResponse({'outfits': data})


def edit_showroom(request, pk):
    if request.method == 'POST':
        try:
            showroom = Showroom.objects.get(pk=pk)
            data = json.loads(request.body)
            new_title = data.get('title', '').strip()

            if new_title:
                showroom.title = new_title
                showroom.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Title is empty'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})                                
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def follow_showroom(request, pk):
    if request.method == 'POST':
        showroom = Showroom.objects.get(pk=pk)
        user_profile = request.user.profile

        ShowroomFollower.objects.create(showroom=showroom, profile=user_profile)
        return JsonResponse({
            'success': True,
            'new_follower_count': showroom.followers.count(),
        })


@login_required
def user_outfits_paginated(request):
    outfits = request.user.profile.outfits.all()
    paginator = Paginator(outfits, 20)  # 20 per page
    page = request.GET.get('page')
    outfits_page = paginator.get_page(page)

    return render(request, 'showrooms/outfit-items.html', {'outfits': outfits_page})