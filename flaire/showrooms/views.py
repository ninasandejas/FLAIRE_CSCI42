from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse

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
    per_page = 4 if page > 1 else 3

    paginator = Paginator(users_showrooms, per_page)
    current_page = paginator.get_page(page)

    showroom_data = [
        {
            "id": showroom.id,
            "title": showroom.title,
            "cover_image": showroom.cover_image.url if showroom.cover_image else "",
        }
        for showroom in current_page.object_list
    ]

    return JsonResponse({
        "showrooms": showroom_data,
        "has_next": current_page.has_next(),
        "has_previous": current_page.has_previous(),
        "current_page": current_page.number,
        "num_pages": paginator.num_pages
    })


@login_required(login_url='user_management:login')
def showroom_detail(request, pk):
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

    return render(request, 'showrooms/showroom-detail.html', {
        'showroom': showroom,
        'accepted_collaborators': accepted_collaborators,
        'outfit_count': outfit_count,
        'follower_count': follower_count,
        'show_follow_button': not (is_follower or is_collaborator or is_owner),
        'show_edit_button': is_owner or is_collaborator,
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
        form.fields['outfits'].queryset = user_profile.outfits.all()

        if form.is_valid():
            showroom = form.save(commit=False)
            showroom.owner = user_profile
            showroom.save()

            collaborators = form.cleaned_data['collaborators']
            for collab in collaborators:
                ShowroomCollaborator.objects.create(
                    showroom=showroom,
                    collaborator=collab,
                    invited_by=user_profile,
                    status='PENDING'
                )

            outfits = form.cleaned_data['outfits']
            for outfit in outfits:
                ShowroomOutfit.objects.create(
                    showroom=showroom,
                    outfit=outfit
                )

            return redirect('showrooms:showroom_detail', pk=showroom.pk)
    else:
        form = ShowroomCreateForm()
        form.fields['outfits'].queryset = user_profile.outfits.all()

    return render(request, 'showrooms/showroom-create.html', {'form': form})


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