from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserProfileForm

# Create your views here.

def user_profile(request):
    """
    View to display the profile of a logged in user.
    Displays an individual instance of
        :model: `UserProfile`
    """

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user_id=request.user)

        if request.method == 'POST':
            form = UserProfileForm(request.POST, instance=user_profile)
            if form.is_valid():
                form.save()
                return redirect('user_profile')
        else:
            form = UserProfileForm(instance=user_profile)

        context = {
            'user_profile': user_profile,
            'form': form
                    }
        return render(request, "profiles/user_profile.html", context)
    else:
        return redirect('login')