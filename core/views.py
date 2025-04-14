from django.shortcuts import render

def home(request):
    
    return render(request, 'core/home.html')

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