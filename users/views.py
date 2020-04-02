from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UCFWithExtends, creationProfile
from .models import Profile

def register(request):
    """Register a new user"""
    if request.method != 'POST':
        form = UCFWithExtends()
    else:
        form = UCFWithExtends(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('bookflix:index')
    context = {'form': form}
    return render(request, 'registration/register.html', context)


def newProfile(request):
    usuario = request.user
    countProfiles = Profile.objects.filter(user=usuario).count()

    if request.method != 'POST':
        form = creationProfile()
    else:
        form = creationProfile(request.POST)
        if form.is_valid():
            if (countProfiles < usuario.subscription.limitProfiles):
                new_profile = form.save(commit=False)
                new_profile.user = usuario
                new_profile.save()
                return redirect('books:index')
            else:
                #acá daría el msg de error: max perfiles permitidos
                return redirect('books:index')

    context = {'form': form}
    return render(request, 'registration/newProfile.html', context)


def viewIndex(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    request.session['myProfile'] = profile_id
    request.session.set_expiry(0)

    context = {'profile': profile}
    return render(request, 'profile.html', context)
