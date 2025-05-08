import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from .forms import *
from .models import *
from social.models import Notification

import json

@login_required(login_url="user_management:login")
def showrooms(request):
    return render(
        request, "showrooms/owned-showrooms.html", {"active_tab": "showrooms"}
    )


@login_required(login_url="user_management:login")
def list_of_showrooms(request):
    users_showrooms = (
        Showroom.objects.filter(
            Q(owner=request.user.profile)
            | Q(
                showroomcollaborator__collaborator=request.user.profile,
                showroomcollaborator__status="ACCEPTED",
            )
        )
        .distinct()
        .order_by("-date_created")
    )

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
    invited_collaborators = ShowroomCollaborator.objects.filter(
        showroom=showroom,
        status='PENDING'
        ).select_related('collaborator')


    is_follower = showroom.followers.filter(id=request.user.profile.id).exists()

    is_collaborator = accepted_collaborators.filter(collaborator=request.user.profile).exists()

    is_invited = invited_collaborators.filter(collaborator=request.user.profile).exists()

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
        'if_following': is_follower,
        'if_invited': is_invited
    })


@login_required(login_url="user_management:login")
def showroom_outfits(request, pk):
    showroom = Showroom.objects.get(pk=pk)
    outfits = showroom.outfits.all()
    data = []
    for outfit in outfits:
        data.append(
            {
                "id": outfit.id,
                "image": outfit.image.url if outfit.image else "",
            }
        )
    return JsonResponse({"outfits": data})


@login_required(login_url="user_management:login")
def create_showroom(request):
    user_profile = request.user.profile

    if request.method == "POST":
        form = ShowroomCreateForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            showroom = form.save(commit=False)
            showroom.owner = user_profile
            showroom.save()

            collaborators = form.cleaned_data.get('collaborators', [])
            for collab in collaborators:
                ShowroomCollaborator.objects.create(
                    showroom=showroom,
                    collaborator=collab,
                    invited_by=user_profile,
                    status="PENDING",
                )
                Notification.objects.create(
                    sender=user_profile,
                    recipient=collab,
                    message=f"You've been invited to collaborate on '{showroom.title}'",
                    link=reverse('showrooms:showroom_detail', kwargs={
                        'pk': showroom.id,
                        'slug': showroom.slug
                    }),
                    is_read=False
                )

            tags = request.POST.get("tags", "").split(",")
            showroom.tags.set(tags[:3])

            return redirect('showrooms:showroom_detail', pk=showroom.id, slug=showroom.slug)

    else:
        form = ShowroomCreateForm(user=request.user)

    return render(request, 'showrooms/showroom-create.html', {
        'form': form
    })
        

@login_required(login_url='user_management:login')
def create_showroom_outfit_modal(request, pk):
    showroom = Showroom.objects.get(pk=pk)
    user_profile = request.user.profile
    user_outfits = user_profile.outfits.all()
    showroom_outfits = showroom.outfits.all()
    
    available_outfits = user_outfits.exclude(
        id__in=showroom_outfits.values_list('id', flat=True))

    data = []
    for outfit in available_outfits:
        data.append({
        'id': outfit.id,
        'image': outfit.image.url if outfit.image else '',
    })
    return JsonResponse({'outfits': data})


@login_required(login_url='user_management:login')
def add_outfit_to_showroom(request, pk):
    if request.method == 'POST':
        user_profile = request.user.profile
        showroom = get_object_or_404(Showroom, pk=pk)

        data = json.loads(request.body)
        outfit_id = data.get('outfit_id')

        try:
            outfit = Outfit.objects.get(pk=outfit_id, owner=user_profile)
            if not showroom.outfits.filter(pk=outfit.pk).exists():
                ShowroomOutfit.objects.create(showroom=showroom, outfit=outfit)
                return JsonResponse({'success': True})
        except Outfit.DoesNotExist:
            pass

        return JsonResponse({'success': False}, status=400)


@login_required(login_url='user_management:login')
def edit_showroom(request, pk):
    if request.method == "POST":
        try:
            showroom = Showroom.objects.get(pk=pk)
            data = json.loads(request.body)
            new_title = data.get("title", "").strip()

            if new_title:
                showroom.title = new_title
                showroom.save()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "error": "Title is empty"})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method"})


@login_required(login_url='user_management:login')
def follow_showroom(request, pk):
    if request.method == "POST":
        showroom = Showroom.objects.get(pk=pk)
        user_profile = request.user.profile

        ShowroomFollower.objects.create(showroom=showroom, profile=user_profile)
        Notification.objects.create(
            sender=user_profile,
            recipient=showroom.owner,
            message=f"{user_profile} followed your showroom, '{showroom.title}'",
            link=reverse('showrooms:showroom_detail', kwargs={
                'pk': showroom.id,
                'slug': showroom.slug
            }),
            is_read=False
        )

        return JsonResponse({
            'success': True,
        })
    
def unfollow_showroom(request, pk):
    if request.method == 'POST':
        showroom = Showroom.objects.get(pk=pk)
        user_profile = request.user.profile

        showroom_follow = ShowroomFollower.objects.get(
            showroom=showroom, 
            profile=user_profile)
        showroom_follow.delete()
        
        return JsonResponse({
            'success': True,
        }) 
    

@login_required(login_url='user_management:login')
def accept_showroom_invite(request, pk):
    if request.method == 'POST':
        showroom = Showroom.objects.get(pk=pk)
        user_profile = request.user.profile

        collaborator = ShowroomCollaborator.objects.get(
            showroom=showroom, 
            collaborator=user_profile, 
            status='PENDING')
        
        remove_notif = Notification.objects.get(
            sender=showroom.owner,
            recipient=user_profile,
            message=f"You've been invited to collaborate on '{showroom.title}'",
            link=reverse('showrooms:showroom_detail', kwargs={'pk': showroom.id, 'slug': showroom.slug}),
        )
        remove_notif.delete()
        
        collaborator.status = 'ACCEPTED'
        collaborator.save()
        
        return JsonResponse({
            'success': True,
        })
    
    
@login_required(login_url='user_management:login')
def decline_showroom_invite(request, pk):
    if request.method == 'POST':
        showroom = Showroom.objects.get(pk=pk)
        user_profile = request.user.profile

        collaborator = ShowroomCollaborator.objects.get(
            showroom=showroom, 
            collaborator=user_profile, 
            status='PENDING')
        
        remove_notif = Notification.objects.get(
            sender=showroom.owner,
            recipient=user_profile,
            message=f"You've been invited to collaborate on '{showroom.title}'",
            link=reverse('showrooms:showroom_detail', kwargs={'pk': showroom.id, 'slug': showroom.slug}),
        )
        remove_notif.delete()
        
        collaborator.status = 'REJECTED'
        collaborator.save()
        
        return JsonResponse({
            'success': True,
        })