
from django import forms
from .models import UserProfile, UserAddress


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile details.
    """
    class Meta:
        model = UserProfile
        fields = ['phone']

    # get fields from the UserProfile model to add to the form
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(
            *args, **kwargs)
        self.fields['first_name'] = forms.CharField(
            max_length=50, required=True)
        self.fields['last_name'] = forms.CharField(
            max_length=50, required=True)
        self.fields['email'] = forms.EmailField(
            max_length=200, required=True)

    def save(self, commit=True):
        """
        Save method to update user's profile details.
        """
        user_profile = super(UserProfileForm, self).save(commit=False)
        # get the current user
        user = user_profile.user_id
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user_profile.save()
        return user_profile


class UserAddressForm(forms.ModelForm):
    """
    Form for updating user profile address(es).
    """
    COUNTRY_CHOICES = [
        ('Ireland', 'Ireland'),
    ]

    country = forms.ChoiceField(choices=COUNTRY_CHOICES, initial='Ireland')

    class Meta:
        model = UserAddress
        fields = ['address_name', 'street_address_1', 'street_address_2', 'town_city', 'county', 'post_code', 'country']
        widgets = {
            'country': forms.Select(attrs={'readonly': 'readonly'}),
        }

        # Set default country value
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['country'].initial = 'IE'
            self.fields['country'].widget.attrs['disabled'] = True

        def clean(self):
            cleaned_data = super().clean()
            return cleaned_data