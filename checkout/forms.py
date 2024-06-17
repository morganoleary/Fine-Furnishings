from django import forms
from .models import Order
from profiles.models import UserAddress, UserProfile

class OrderForm(forms.ModelForm):
    full_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    street_address1 = forms.CharField(max_length=255, required=True)
    street_address2 = forms.CharField(max_length=255, required=False)
    town_or_city = forms.CharField(max_length=100, required=True)
    county = forms.CharField(max_length=100, required=True)
    postcode = forms.CharField(max_length=20, required=True)
    country = forms.CharField(max_length=100, required=True)
    
    class Meta:
        model = Order
        fields = (
            'full_name',
            'email',
            'phone_number',
            'street_address1',
            'street_address2',
            'town_or_city',
            'county',
            'postcode',
            'country',
        )

    def __init__(self, user_profile=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if user_profile:
            profile = user_profile.user_id
            self.fields['full_name'].initial = f"{profile.first_name} {profile.last_name}"
            self.fields['email'].initial = profile.email
            self.fields['phone_number'].initial = user_profile.phone
            
            addresses = UserAddress.objects.filter(user_profile=user_profile)
            if addresses.exists():
                address = addresses.first()
                self.fields['street_address1'].initial = address.street_address_1
                self.fields['street_address2'].initial = address.street_address_2
                self.fields['town_or_city'].initial = address.town_city
                self.fields['county'].initial = address.county
                self.fields['postcode'].initial = address.post_code
                self.fields['country'].initial = address.country

        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'town_or_city': 'Town or City',
            'county': 'County',
            'postcode': 'Postal Code',
            'country': 'Country',
        }

        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = placeholders[field]
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False