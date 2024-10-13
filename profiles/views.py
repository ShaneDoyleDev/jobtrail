from django.shortcuts import redirect, render
from django.contrib import messages

from .models import Profile
from .forms import ProfileForm


def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        # Grab data from form
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('dashboard')
        else:
        
            form = ProfileForm(request.POST, instance=profile)
            messages.error(request, "Somethings wrong. Profile not updated.")
            
    else:
        form = ProfileForm(instance=profile)
        
    return render(request, 'profiles/profile_update.html', {'form': form})
