from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import SignUpForm


# Create your views here.
def front_page(request):
    return render(request, 'core/front_page.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('front_page')
        else:
            return render(request, 'core/signup.html', {'form': form})
    else:
        form = SignUpForm()

        return render(request, 'core/signup.html', {'form': form})
