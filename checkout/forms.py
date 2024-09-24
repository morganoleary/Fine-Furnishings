from django import forms
from .models import Order
from profiles.models import UserAddress, UserProfile

# Define country choices with only Ireland ("IE")
COUNTRY_CHOICES = [
    ('IE', 'Ireland'),
]

class OrderForm(forms.ModelForm):
    """ 
    A form to allow the user to fill out their details during checkout
    """
    full_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    street_address1 = forms.CharField(max_length=255, required=True)
    street_address2 = forms.CharField(max_length=255, required=False)
    town_or_city = forms.CharField(max_length=100, required=True)
    county = forms.CharField(max_length=100, required=True)
    postcode = forms.CharField(max_length=20, required=True)
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, required=True, widget=forms.Select(attrs={'readonly': 'readonly'}))
    address_choices = forms.ChoiceField(choices=[], required=False)
    address_name = forms.CharField(max_length=50, required=False)
    
    class Meta:
        model = Order
        fields = (
            'full_name',
            'email',
            'phone_number',
            'address_choices',
            'address_name',
            'street_address1',
            'street_address2',
            'town_or_city',
            'county',
            'postcode',
            'country',
        )

    def __init__(self, user_profile=None, *args, **kwargs):
        selected_address = kwargs.pop('selected_address', None)
        super().__init__(*args, **kwargs)

        if user_profile:
            user = user_profile.user_id
            self.fields['full_name'].initial = f"{user.first_name} {user.last_name}"
            self.fields['email'].initial = user.email
            self.fields['phone_number'].initial = user_profile.phone

            address_choices = [(address.id, address.address_name) for address in UserAddress.objects.filter(user_profile=user_profile)]
            self.fields['address_choices'].choices = [('', 'Select an address')] + address_choices
            
            if selected_address:
                address = UserAddress.objects.get(id=selected_address)
                self.fields['street_address1'].initial = address.street_address_1
                self.fields['street_address2'].initial = address.street_address_2
                self.fields['town_or_city'].initial = address.town_city
                self.fields['county'].initial = address.county
                self.fields['postcode'].initial = address.post_code
                self.fields['country'].initial = 'IE'
                self.fields['country'].widget.attrs['disabled'] = True

        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'address_name': 'Address Name',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'town_or_city': 'Town or City',
            'county': 'County',
            'postcode': 'Postal Code',
            'country': 'Country',
        }

        for field in self.fields:
            if field != 'address_choices':
                self.fields[field].widget.attrs['placeholder'] = placeholders[field]
                self.fields[field].widget.attrs['class'] = 'stripe-style-input'
                self.fields[field].label = False
    
    def save(self, commit=True):
        """
        Override the save method to include user details in the Order model.
        """
        order = super().save(commit=False)
        order.user_name = self.cleaned_data['full_name']
        order.user_email = self.cleaned_data['email']
        order.user_phone = self.cleaned_data['phone_number']

        if commit:
            order.save()
            
            # Handle address
            address_id = self.cleaned_data.get('address_choices')
            if address_id:
                try:
                    address = UserAddress.objects.get(id=address_id)
                    order.address = address
                except UserAddress.DoesNotExist:
                    pass
            else:
                # Update address with the form data
                address_name = self.cleaned_data['address_name']
                address_data = {
                    'street_address_1': self.cleaned_data['street_address1'],
                    'street_address_2': self.cleaned_data['street_address2'],
                    'town_city': self.cleaned_data['town_or_city'],
                    'county': self.cleaned_data['county'],
                    'post_code': self.cleaned_data['postcode'],
                    'country': self.cleaned_data['country'],
                }
                user_address, created = UserAddress.objects.update_or_create(
                    user_profile=order.user_profile,
                    address_name=address_name,
                    defaults=address_data,
                )
                order.address = user_address
            
            order.save()
        return order