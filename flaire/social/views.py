from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from apps.users.models import Profile
from apps.outfits.models import Outfit
from apps.showrooms.models import Showroom
