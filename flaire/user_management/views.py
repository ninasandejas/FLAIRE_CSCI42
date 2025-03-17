from django.db.models.base import Model 
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView, CreateView
from django.views import View
from .models import Profile
from .forms import LoginForm, SignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.urls import reverse_lazy


# class UserUpdateView(LoginRequiredMixin, UpdateView):
#     model = Profile
#     form_class = ProfileForm
#     template_name = 'user_detail.html'
#     success_url = reverse_lazy('homepage:homepage')

#     def get_object(self, queryset=None):
#         return self.request.user.profile
    
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)

class UserLoginView(FormView):
    model = User
    template_name = "registration/login.html"
    form_class = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('placeholder')  # Redirect to homepage after successful login


class UserCreateView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        
        Profile.objects.create(
            user=user,
            display_name=user.username, 
            email_address=user.email  
        )

        login(self.request, user)  

        return redirect(self.success_url)
    
    
class PlaceholderView(View):
    def get(self, request):
        return render(request, "placeholder.html")