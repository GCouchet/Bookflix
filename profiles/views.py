from django.shortcuts import render, redirect
from .forms import creationProfile
from .models import Profile

def newProfile(request):
    usuario = request.user
    countProfiles = Profile.objects.filter(user=usuario).count()
    if request.method != 'POST':
        # se muestra un form en blanco para registrarlo
        form = creationProfile()
    else:
        # se procesa un form completado
        form = creationProfile(request.POST)
        if form.is_valid():
            if (not usuario.subscription is None) and (countProfiles < usuario.subscription.limitProfiles):
                new_profile = form.save(commit=False)
                new_profile.user = usuario
                new_profile.save()
                return redirect('books:index')
            else:
                #acá daría el msg de error: max perfiles permitidos
                return redirect('books:index')

    context = {'form': form}
    return render(request, 'newProfile.html', context)


def deleteProfile(request, profile_id):
    Profile.objects.filter(id=profile_id).delete()
    return redirect(request.path)


def selectProfile(request):
    profiles = Profile.objects.all()
    profiles = profiles.filter(user=request.user)
    context = {'profiles': profiles}
    return render(request, 'selectProfile.html', context)


def viewIndex(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    request.session['myProfile'] = profile_id
    #request.session.set_expiry(0) ¿como borro el atributo (del request.session['myProfile'])

    context = {'profile': profile}
    return render(request, 'profile.html', context)