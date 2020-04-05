from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UCFWithExtends

def register(request):
    """Register a new user"""
    if request.method != 'POST':
        form = UCFWithExtends()
    else:
        form = UCFWithExtends(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('books:index')
    context = {'form': form}
    return render(request, 'registration/register.html', context)
