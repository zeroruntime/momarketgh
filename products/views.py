from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import ProductListing

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProductListingForm 
from .models import ProductListing

def market_view(request):
    products = ProductListing.objects.filter(is_active=True).select_related('user').order_by('-created_at')
    return render(request, 'products/market.html', {'products': products})

 
@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ProductListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()

            # Save multiple photos
            photos = request.FILES.getlist('photos')
            from .models import ProductPhoto
            for photo in photos:
                ProductPhoto.objects.create(product_listing=listing, photo=photo)

            messages.success(request, 'Your product has been listed successfully!')
            return redirect('/') 
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductListingForm()
    
    return render(request, 'products/create_listing.html', {'form': form})

def product_detail(request, slug, uid):
    product = get_object_or_404(ProductListing, slug=slug, is_active=True, uid=uid)
    similar_products = ProductListing.objects.filter(
        region=product.region
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'similar_products': similar_products,
    }
    return render(request, 'products/product_detail.html', context)

@login_required
@require_POST
def product_delete(request, pk):
    listing = get_object_or_404(ProductListing, pk=pk, user=request.user)
    listing.delete()
    return redirect('farmer_dashboard')
