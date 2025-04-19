from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from transport.models import TransporterProfile
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.views import LogoutView


def register(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        role = request.POST.get('role')
        region = request.POST.get('region')
        location = request.POST.get('location')

        # Validate passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/register.html', {
                'role': role,
                'full_name': full_name,
                'username': username,
                'phone_number': phone_number,
                'region': region,
                'location': location,
            })

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, 'accounts/register.html', {
                'role': role,
                'full_name': full_name,
                'username': '',
                'phone_number': phone_number,
                'region': region,
                'location': location,
            })

        # Create user
        user = User.objects.create_user(
            username=username,
            password=password1,
            full_name=full_name,
            phone_number=phone_number,
            role=role,
            region=region,
            location=location
        )

        user.is_active = True
        user.save()

        # If transporter, create transporter profile
        if role == 'Transporter':
            TransporterProfile.objects.create(
                user=user,
                vehicle_type='',
                route_regions='',
                pricing_note='',
                contact_number=phone_number,
                is_available=True
            )

        # Log the user in
        user = authenticate(request, username=username, password=password1)
        if user:
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('profile')
        else:
            messages.error(request, "There was a problem logging you in.")
            return redirect('login')


    return render(request, 'accounts/register.html')

class CustomLoginView(LoginView):
    def form_valid(self, form):
        remember = self.request.POST.get('remember')
        user = form.get_user()
        
        # Set session expiry based on "remember me"
        if remember:
            # Remember me checked → persistent session (2 weeks)
            self.request.session.set_expiry(60 * 60 * 24 * 30)  # 2 weeks in seconds
        else:
            # Not checked → expire when browser closes
            self.request.session.set_expiry(0)

        messages.success(self.request, f"Welcome back, {user.full_name}!" if user.full_name else f"Welcome back, {user.username}!")
        return super().form_valid(form)
    

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You’ve been logged out successfully.")
        return super().dispatch(request, *args, **kwargs)



@login_required
def profile_view(request):
    user = request.user
    context = {
        'user': user,
        'is_transporter': hasattr(user, 'transporterprofile')
    }
    
    if user.role == 'Transporter':
        context['transporter_profile'] = user.transporterprofile
    
    return render(request, 'accounts/profile.html', context)

@login_required
def profile_update(request):
    user = request.user
    
    if request.method == 'POST':
        user.full_name = request.POST.get('full_name', user.full_name)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.region = request.POST.get('region', user.region)
        user.location = request.POST.get('location', user.location)
        
        # Update password if provided
        new_password = request.POST.get('new_password')
        if new_password:
            user.set_password(new_password)
        
        user.save()
        
        # Update transporter profile if applicable
        if user.role == 'Transporter':
            transporter_profile = user.transporterprofile
            transporter_profile.vehicle_type = request.POST.get('vehicle_type', transporter_profile.vehicle_type)
            transporter_profile.route_regions = request.POST.get('route_regions', transporter_profile.route_regions)
            transporter_profile.pricing_note = request.POST.get('pricing_note', transporter_profile.pricing_note)
            transporter_profile.contact_number = request.POST.get('contact_number', transporter_profile.contact_number)
            transporter_profile.is_available = request.POST.get('is_available') == 'on'
            transporter_profile.save()
        
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')
    
    context = {
        'user': user,
        'regions': [
            'Greater Accra', 'Ashanti', 'Eastern', 'Western', 'Central',
            'Northern', 'Upper East', 'Upper West', 'Volta', 'Bono',
            'Bono East', 'Ahafo', 'Western North', 'Oti', 'Savannah', 'North East'
        ]
    }
    
    if user.role == 'Transporter':
        context['transporter_profile'] = user.transporterprofile
    
    return render(request, 'accounts/profile_update.html', context)

def unauthorized_view(request):
    return render(request, "accounts/403.html", status=403)

# def farmer_list(request):
#     farmers = User.objects.filter(role='Farmer')
#     return render(request, 'accounts/farmer_list.html', {'farmers': farmers})

# def trader_list(request):
#     traders = User.objects.filter(role='Trader')
#     return render(request, 'accounts/trader_list.html', {'traders': traders})

# def transporter_list(request):
#     transporters = User.objects.filter(role='Transporter')
#     return render(request, 'accounts/transporter_list.html', {'transporters': transporters})