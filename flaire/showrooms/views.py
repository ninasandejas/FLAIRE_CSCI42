from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse

from .forms import *
from .models import *

@login_required(login_url='user_management:login')
def showrooms(request):
    return render(request, "showrooms/owned-showrooms.html", {"active_tab": "showrooms"})


@login_required(login_url='user_management:login')
def list_of_showrooms(request):
    users_showrooms = Showroom.objects.filter(
        Q(owner=request.user.profile) |
        Q(collaborators=request.user.profile)        
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
    return render(request, 'showrooms/showroom-detail.html', {
        'showroom': showroom,
        'outfit_count': outfit_count,
        'follower_count': follower_count,
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