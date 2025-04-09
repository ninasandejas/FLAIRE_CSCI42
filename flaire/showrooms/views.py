from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse

# from .forms import *
from .models import *

@login_required(login_url='user_management:login')
def showrooms(request):
    return render(request, "showrooms/owned-showrooms.html", {"active_tab": "showrooms"})


@login_required(login_url='user_management:login')
def list_of_showrooms(request):
    # user = request.user.profile
    users_showrooms = Showroom.objects.filter(
        Q(owner=request.user.profile) |
        Q(collaborators=request.user.profile)        
        # models.Q(owner = user |
        # models.Q(collaborators = user)
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