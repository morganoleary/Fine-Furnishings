from django.shortcuts import render

# Create your views here.
def home(request):
    """ A view to return the home page """
    
    return render(request, 'home/home_page.html')


def faq(request):
    """ A view to return the FAQ page """

    return render(request, 'home/faq.html')

