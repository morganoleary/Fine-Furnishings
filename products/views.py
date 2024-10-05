from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm

# The all_products view code was implemented with the help of the 
# Boutique Ado project walkthrough to implement the search bar's functionality
# and category filtering
def all_products(request):
    """ A view to render all products """

    products = Product.objects.all()
    query = None
    categories = None

    if request.GET:
        if 'categories' in request.GET:
            categories = request.GET['categories'].split(',')
            products = products.filter(categories__name__in=categories).distinct()
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "Please enter your search request.")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query) | Q(categories__name__icontains=query)
            products = products.filter(queries).distinct()

            if not products.exists():
                messages.info(request, f'No products found for "{query}".')

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

    products = Product.objects.filter(categories__name__iexact='sofa').distinct()
    context = {'products': products, 'category': 'Sofas'}
    return render(request, 'products/products.html', context)


def bedroom_products(request):
    """ A view to render the bedroom category of products """
    
    products = Product.objects.filter(categories__name__iexact='bedroom').distinct()
    context = {'products': products, 'category': 'Bedroom'}
    return render(request, 'products/products.html', context)


def dining_products(request):
    """ A view to render the dining category of products """
    
    products = Product.objects.filter(categories__name__iexact='dining').distinct()
    context = {'products': products, 'category': 'Dining'}
    return render(request, 'products/products.html', context)


# The product CRUD functionality (add, edit, delete) implemented for site admins was implemented
# with the help of the Boutique Ado Walkthrough - Product Admin

@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store administrators can add a product.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store administrators can edit products.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing "{product.name}"')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store administrators can delete products.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, f'"{product.name}" deleted!')
    return redirect(reverse('products'))