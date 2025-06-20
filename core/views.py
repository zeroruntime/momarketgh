from django.shortcuts import render
from datetime import timedelta, date
from django.db.models import Avg
from django.utils import timezone

from products.models import ProductListing

def get_price_trends():
    today = timezone.now()
    last_week_start = today - timedelta(days=7)
    previous_week_start = today - timedelta(days=14)

    # Now filter using timezone-aware datetimes
    last_week_data = ProductListing.objects.filter(
        is_active=True,
        created_at__gte=last_week_start,
        created_at__lt=today
    ).values('crop__name', 'region').annotate(avg_price=Avg('price_per_unit'))

    prev_week_data = ProductListing.objects.filter(
        is_active=True,
        created_at__gte=previous_week_start,
        created_at__lt=last_week_start
    ).values('crop__name', 'region').annotate(avg_price=Avg('price_per_unit'))

    # Map previous week prices
    prev_map = {
        (item['crop__name'], item['region']): item['avg_price']
        for item in prev_week_data
    }

    # Calculate trend
    trends = []
    for item in last_week_data:
        key = (item['crop__name'], item['region'])
        current = item['avg_price']
        previous = prev_map.get(key)

        trend = ((current - previous) / previous) * 100 if previous else 0

        trends.append({
            'crop_name': item['crop__name'],
            'region': item['region'],
            'average_price': round(current, 2),
            'trend': round(trend, 1)
        })

    return trends


def home(request):
    featured_products = ProductListing.objects.filter(is_active=True).order_by('-created_at')[:8]
    price_trends = get_price_trends()


    return render(request, 'core/home.html', {
        'featured_products': featured_products,
        'price_trends': price_trends,
    })

# def about(request):
#     """About page with information about FindMeGH"""
#     return render(request, 'core/about.html')

# def contact(request):
#     """Contact page"""
#     return render(request, 'core/contact.html')

# def privacy_policy(request):
#     """Privacy policy page"""
#     return render(request, 'core/privacy_policy.html')

# def terms_of_service(request):
#     """Terms of service page"""
#     return render(request, 'core/terms_of_service.html')

# def faq(request):
#     """Frequently asked questions page"""
#     return render(request, 'core/faq.html')