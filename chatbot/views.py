import json
import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.db.models import Q, Avg
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta

# Import your models (adjust the import path based on your app structure)
from products.models import Crop, CropCategory, ProductListing
from django.views.decorators.clickjacking import xframe_options_exempt


# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

class KwasiChatbot:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
    def get_system_prompt(self, user_context=None):
        """Enhanced system prompt for agricultural assistance"""
        base_prompt = """
        You are Kwasi, a helpful agricultural assistant for MoMarket GH created by Emmanuel Aforo and Stesha Quarcoo, members of the PRESEC Robotics and Programming Club, a platform connecting farmers, traders in Ghana eliminating the need for middlemen.
        
        Your personality:
        - Friendly, knowledgeable, and supportive
        - Speak like a helpful Ghanaian agricultural expert, refrain from abusing the word "Akwaaba" or "Sankofa", using it only when appropriate
        - Use local terms and references where relevant
        - Mention your name once per conversation to establish identity
        - Avoid slang or overly casual language 
        - Use simple, clear language
        - Be encouraging and positive
        
        Your main functions:
        1. Help users navigate the platform
        2. Provide agricultural advice (farming tips, crop information, seasonal guidance)
        3. Assist with pricing and market insights
        4. Help with crop listings and searches
        5. Answer questions about farming practices in Ghana
        
        Keep responses concise but helpful. Always be respectful and professional.
        If you don't know something specific, admit it and suggest they contact support or consult local agricultural experts.
        """
        
        if user_context:
            base_prompt += f"\n\nUser context: {user_context}"
            
        return base_prompt
    
    def get_crop_data_context(self, query):
        """Get relevant crop data based on user query"""
        context = []
        
        # Search for crops mentioned in query
        crops = Crop.objects.filter(
            Q(name__icontains=query) | 
            Q(category__name__icontains=query)
        )[:5]
        
        if crops:
            context.append("Available crops on platform:")
            for crop in crops:
                # Get recent listings for this crop
                recent_listings = ProductListing.objects.filter(
                    crop=crop, 
                    is_active=True,
                    created_at__gte=timezone.now() - timedelta(days=30)
                )[:3]
                
                avg_price = recent_listings.aggregate(avg_price=Avg('price_per_unit'))['avg_price']
                
                crop_info = f"- {crop.name} ({crop.category.name})"
                if avg_price:
                    crop_info += f" - Average price: GH₵{avg_price:.2f}"
                if recent_listings:
                    regions = set(listing.region for listing in recent_listings)
                    crop_info += f" - Available in: {', '.join(list(regions)[:3])}"
                
                context.append(crop_info)
        
        return "\n".join(context) if context else ""
    
    def get_market_insights(self, region=None):
        """Get current market insights"""
        insights = []
        
        # Get most active crops
        popular_crops = ProductListing.objects.filter(
            is_active=True,
            created_at__gte=timezone.now() - timedelta(days=7)
        ).values('crop__name').distinct()[:5]
        
        if popular_crops:
            crop_names = [crop['crop__name'] for crop in popular_crops]
            insights.append(f"Recently active crops: {', '.join(crop_names)}")
        
        # Regional data if specified
        if region:
            regional_listings = ProductListing.objects.filter(
                region__icontains=region,
                is_active=True,
                created_at__gte=timezone.now() - timedelta(days=14)
            ).count()
            
            if regional_listings:
                insights.append(f"Current listings in {region}: {regional_listings}")
        
        return "\n".join(insights) if insights else ""
    
    # def generate_response(self, user_message, user_context=None):
    #     try:
    #         crop_context = self.get_crop_data_context(user_message)
    #         market_context = self.get_market_insights()
    #         system_prompt = self.get_system_prompt(user_context)

    #         full_prompt = f"""
    #         {system_prompt}
            
    #         Current platform data:
    #         {crop_context}
            
    #         Market insights:
    #         {market_context}
            
    #         User question: {user_message}
            
    #         Provide a helpful response as Kwasi, the agricultural assistant.
    #         """

    #         print("KWASI Prompt Length:", len(full_prompt))
    #         print("KWASI Prompt Preview:", full_prompt[:500])  # Avoid printing everything
    #         response = self.model.generate_content(full_prompt)
    #         return response.text

    #     except Exception as e:
    #         print("KWASI ERROR:", str(e))  # This will show the actual problem
    #         return "Sorry, I'm having trouble processing your request right now. Please try again or contact our support team."

    def generate_response(self, user_message, user_context=None, history=None):
        try:
            crop_context = self.get_crop_data_context(user_message)
            market_context = self.get_market_insights()
            system_prompt = self.get_system_prompt(user_context)

            # Build a single string prompt
            history_text = ""
            if history:
                for turn in history[-10:]:
                    prefix = "User:" if turn["role"] == "user" else "Assistant:"
                    history_text += f"{prefix} {turn['content']}\n"

            full_prompt = f"""
            {system_prompt}

            Conversation history:
            {history_text}

            Current platform data:
            {crop_context}

            Market insights:
            {market_context}

            User question: {user_message}

            Respond as Kwasi, the helpful Ghanaian agricultural assistant.
            """

            response = self.model.generate_content(full_prompt)
            return response.text

        except Exception as e:
            print("KWASI ERROR:", str(e))
            return "Sorry, I'm having trouble processing your request right now. Please try again or contact our support team."

# Initialize chatbot
kwasi = KwasiChatbot()

@csrf_exempt
@require_http_methods(["POST"])
@xframe_options_exempt
def chat_with_kwasi(request):
    """Handle chat messages"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        history = data.get('history', [])

        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)

        user_context = None
        if request.user.is_authenticated:
            user_context = f"User is logged in as {request.user.username}"

        bot_response = kwasi.generate_response(user_message, user_context, history)

        return JsonResponse({
            'response': bot_response,
            'timestamp': timezone.now().isoformat()
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        print("KWASI ERROR:", str(e))
        return JsonResponse({'error': 'Internal server error'}, status=500)

@xframe_options_exempt
def chatbot_widget(request):
    """Render the chatbot widget"""
    return render(request, 'chatbot/widget.html')