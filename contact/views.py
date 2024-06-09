from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

# Create your views here.


def contact_form(request):
    """
    View to handle contact form submission.
    **Context**
    ``contact_form``
        An instance of :form: `contact.ContactForm`
    **Template**
    :template: `contact/contact_form.html`
    """
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,messages.SUCCESS,
                'Your message has been sent!'
            )
            return redirect('contact')

    else:
        form = ContactForm()

    return render(
        request,
        "contact/contact_form.html",
        {
            "contact_form": form
        }
    )