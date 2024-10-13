from django.shortcuts import redirect, render
from django.contrib import messages

from .models import Profile
from .forms import ProfileForm


def profile_update(request):
    # Get or create the user's profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Grab data from form
        form = ProfileForm(request.POST, instance=profile)
        
        if form.is_valid():
            # Ensure the user is set correctly
            form.instance.user = request.user
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('dashboard')
        else:
            messages.error(request, "Something went wrong. Profile not updated.")
    else:
        form = ProfileForm(instance=profile)
        
    return render(request, 'profiles/profile_update.html', {'form': form})
