from django.shortcuts import render


def closet(request):
    return render(request, "closet/outfit-builder.html", {"active_tab": "closet"})


def home(request):
    return render(request, "home.html", {"active_tab": "home"})
