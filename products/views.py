from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category

# The all_products view code was implemented with the help of the 
# Boutique Ado project walkthrough to implement the search bar's functionality
# and category filtering
def all_products(request):
    """ A view to render all products """

    products = Product.objects.all()
    query = None
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "Please enter your search request.")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query) | Q(categories__name__icontains=query)
            products = products.filter(queries).distinct()

            if not products.exists():
                messages.info(request, f'No products found for "{query}"')

    context = {
        'products': products,
        'search_term': query,
        'selected_categories': categories,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to render an individual product's details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


def sofa_products(request):
    """ A view to render the sofas category of products """

    products = Product.objects.filter(categories__name__iexact='sofa')
    context = {'products': products, 'category': 'Sofas'}
    return render(request, 'products/products.html', context)


def bedroom_products(request):
    """ A view to render the bedroom category of products """
    
    products = Product.objects.filter(categories__name__iexact='bedroom')
    context = {'products': products, 'category': 'Bedroom'}
    return render(request, 'products/products.html', context)


def dining_products(request):
    """ A view to render the dining category of products """
    
    products = Product.objects.filter(categories__name__iexact='dining')
    context = {'products': products, 'category': 'Dining'}
    return render(request, 'products/products.html', context)