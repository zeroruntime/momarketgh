from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ProductListing, WhatsAppClick, PriceHistory
from django.utils.timezone import now, timedelta
from django.db.models import Count

@login_required
def farmer_dashboard(request):
    # ✅ Ensure the user is a Farmer
    if request.user.role != 'Farmer':
        return redirect('unauthorized')  # or return a 403 page

    user = request.user

    # Active Listings (with clicks count)
    active_listings = ProductListing.objects.filter(user=user, is_active=True).annotate(
        view_count=Count('whatsappclick')
    )

    # Price Comparisons
    price_comparisons = []
    product_listings = ProductListing.objects.filter(user=user)
    for listing in product_listings:
        market_avg = PriceHistory.objects.filter(
            crop_name=listing.crop_name,
            region=listing.region
        ).order_by('-calculated_on').first()

        price_comparisons.append({
            'name': listing.crop_name,
            'your_price': listing.price_per_unit,
            'market_price': market_avg.average_price if market_avg else listing.price_per_unit
        })

    # Top Performing Crops
    top_crops = ProductListing.objects.filter(region=user.region).values('crop_name').annotate(
        crop_count=Count('id')
    ).order_by('-crop_count')[:5]

    # Views & Clicks Chart
    days_ago_7 = now() - timedelta(days=7)
    labels = []
    views_data = []
    clicks_data = []
    for i in range(7):
        day = days_ago_7 + timedelta(days=i)
        labels.append(day.strftime('%a'))
        views_data.append(WhatsAppClick.objects.filter(timestamp__date=day.date()).count())
        clicks_data.append(WhatsAppClick.objects.filter(timestamp__date=day.date()).count())

    chart_data = {
        'labels': labels,
        'views': views_data,
        'clicks': clicks_data
    }

    context = {
        'active_listings': active_listings,
        'price_comparisons': price_comparisons,
        'top_crops': top_crops,
        'chart': chart_data,
    }

    return render(request, 'analytics/farmer_dashboard.html', context)
