from django.shortcuts import render


def closet(request):
    return render(request, "closet/outfit-builder.html", {"active_tab": "closet"})
