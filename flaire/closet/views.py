from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='user_management:login')
def closet(request):
    return render(request, "closet/outfit-builder.html", {"active_tab": "closet"})
