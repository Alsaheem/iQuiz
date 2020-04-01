from django.shortcuts import render, get_object_or_404, redirect, reverse

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


from django.http import HttpResponse,HttpResponseRedirect
from django.core.exceptions import ValidationError

from django.contrib import messages 

from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import TemplateResponseMixin, View

from .forms import UserForm


@login_required
def dashboard(request):
    user = request.user
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        return redirect('user:dashboard')
    context = {
        "user": user,
    }
    return render(request, 'profile/profile.html', context)


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('quiz:subjects')
            else:
                return render(request, 'registration/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'registration/login.html', {'error_message': 'Invalid login'})
    return render(request, 'registration/login.html')



def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('quiz:home'))

class register(View):
    form_class =UserForm
    template_name = 'accounts/register.html'

    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user =form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user.set_password(password)

            user.save()

            user = authenticate(username=username, password=password)
            messages.success(request, 'thanks for registering')

            if user is not None:

                if user.is_active:
                    login(request,user)
                    return redirect('user:login')
        else:
            # form = UserForm()
            return render(request, 'registration/register.html', {'error_message': 'invalid details, check them again'})


        return render(request, 'registration/register.html', {'form': form})
