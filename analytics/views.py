from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ProductListing, WhatsAppClick, PriceHistory
from django.utils.timezone import now, timedelta
from django.db.models import Count

@login_required
def farmer_dashboard(request):
    # ensure the user is a Farmer
    if request.user.role != 'Farmer':
        return redirect('unauthorized')

    user = request.user

    # shows active listings and counts clicks 
    active_listings = ProductListing.objects.filter(user=user, is_active=True).annotate(
        view_counts=Count('whatsappclick')
    )

    # compares the prices of the user's listings with the market average
    price_comparisons = []
    product_listings = ProductListing.objects.filter(user=user)
    for listing in product_listings:
        market_avg = PriceHistory.objects.filter(
            crop_name=listing.crop.name,
            region=listing.region
        ).order_by('-calculated_on').first()

        price_comparisons.append({
            'name': listing.crop.name,
            'your_price': listing.price_per_unit,
            'market_price': market_avg.average_price if market_avg else listing.price_per_unit
        })

    # logic for showing the top performing crops based on the number of active listings in the user's region
    top_crops = ProductListing.objects.filter(region=user.region).values('crop__name').annotate(
        crop_count=Count('id')
    ).order_by('-crop_count')[:5]

    # logic for showing the number of clicks on the user's listings over the last 7 day and the number of clicks on the WhatsApp link
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
