import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


from analytics.models import WhatsAppClick
from .forms import ProductListingForm 
from .models import ProductListing
from .models import CropCategory, Crop, ProductListing

def crop_categories(request):
    categories = CropCategory.objects.all().prefetch_related('crops')
    for category in categories:
        for crop in category.crops.all():
            crop.active_listings_count = crop.listings.filter(is_active=True).count()
    return render(request, 'products/crop_categories.html', {'categories': categories})

def crop_listings(request, crop_slug):
    crop = Crop.objects.get(slug=crop_slug)
    
    # Get filter parameters
    region = request.GET.get('region', '')
    min_quantity = request.GET.get('min_quantity', '')
    max_price = request.GET.get('max_price', '')
    
    # Start with all active listings for this crop
    listings = ProductListing.objects.filter(crop=crop, is_active=True).order_by('-created_at')
    
    # Apply filters if provided
    if region:
        listings = listings.filter(region=region)
    if min_quantity:
        listings = listings.filter(quantity__gte=float(min_quantity))
    if max_price:
        listings = listings.filter(price_per_unit__lte=float(max_price))
    
    # Get unique regions for the filter
    all_regions = ProductListing.objects.filter(crop=crop).values_list('region', flat=True).distinct()
    
    context = {
        'crop': crop,
        'listings': listings,
        'all_regions': all_regions,
        'selected_region': region,
        'min_quantity': min_quantity,
        'max_price': max_price
    }
    
    return render(request, 'products/crop_listings.html', context)

@csrf_exempt
def track_whatsapp_click(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        listing_id = data.get('listing_id')
        
        try:
            listing = ProductListing.objects.get(id=listing_id)
            
            # Increment the WhatsApp click counter
            listing.whatsapp_click_count += 1
            listing.save()
            
            # Also record the click with user info if available
            if request.user.is_authenticated:
                WhatsAppClick.objects.create(
                    listing=listing,
                    clicked_by=request.user
                )
            else:
                WhatsAppClick.objects.create(
                    listing=listing
                )
                
            return JsonResponse({'status': 'success'})
        except ProductListing.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Listing not found'}, status=404)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

# def market_view(request):
#     products = ProductListing.objects.filter(is_active=True).select_related('user').order_by('-created_at')
#     return render(request, 'products/market.html', {'products': products})

 
@login_required
def create_listing(request):
    crops = Crop.objects.all()


    if request.method == 'POST':
        form = ProductListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            messages.success(request, 'Your product has been listed successfully!')
            return redirect('/') 
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductListingForm()
    
    return render(request, 'products/create_listing.html', {'form': form, 'crops': crops})

def product_detail(request, slug, uid):
    product = get_object_or_404(
        ProductListing, 
        crop__slug=slug, 
        is_active=True, 
        uid=uid
    )
    similar_products = ProductListing.objects.filter(
            region=product.region
        ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'similar_products': similar_products,
    }
    return render(request, 'products/product_detail.html', context)
