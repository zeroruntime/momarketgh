from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Max, Count, Case, When, IntegerField
from .models import Conversation, Message
from products.models import ProductListing
import json

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(
        participants=request.user
    ).annotate(
        last_message_time=Max('message__timestamp'),
        unread_count=Count(
            Case(
                When(
                    Q(message__is_read=False) & ~Q(message__sender=request.user),
                    then=1
                ),
                output_field=IntegerField()
            )
        )
    ).order_by('-last_message_time')

    for convo in conversations:
        convo.other_user = convo.get_other_participant(request.user)
        convo.last_message = convo.get_last_message()
        
    return render(request, 'chat/inbox.html', {
        'conversations': conversations
    })

@login_required  
def conversation_detail(request, uuid):
    conversation = get_object_or_404(Conversation, uuid=uuid)
    
    if request.user not in conversation.participants.all():
        return redirect('inbox')
    
    # Mark messages as read
    conversation.message_set.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    
    other_user = conversation.get_other_participant(request.user)
    
    return render(request, 'chat/conversation.html', {
        'conversation': conversation,
        'messages': conversation.message_set.all(),
        'other_user': other_user,
    })

@login_required
def start_chat(request, product_uid):
    listing = get_object_or_404(ProductListing, uid=product_uid)
    farmer = listing.user
    trader = request.user

    if farmer == trader:
        return redirect('market')

    conversation = Conversation.objects.filter(
        participants=farmer
    ).filter(
        participants=trader
    ).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(farmer, trader)

    return redirect('conversation_detail', uuid=conversation.uuid)

@login_required
@require_http_methods(["POST"])
def send_message(request):
    try:
        data = json.loads(request.body)
        conversation_uuid = data.get('conversation_uuid')
        text = data.get('text', '').strip()
        
        if not text:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)

        conversation = get_object_or_404(Conversation, uuid=conversation_uuid)

        if request.user not in conversation.participants.all():
            return JsonResponse({'error': 'Unauthorized'}, status=403)

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            text=text
        )
        
        # Update conversation timestamp
        conversation.save()
        
        return JsonResponse({
            'success': True,
            'message': {
                'id': message.id,
                'text': message.text,
                'sender': message.sender.id,
                'sender_name': message.sender.get_full_name() or message.sender.username,
                'timestamp': message.timestamp.isoformat()
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Server error'}, status=500)

@login_required
def get_messages(request, uuid):
    conversation = get_object_or_404(Conversation, uuid=uuid)
    
    if request.user not in conversation.participants.all():
        return JsonResponse({'error': 'Forbidden'}, status=403)

    messages = []
    for message in conversation.message_set.all():
        messages.append({
            'id': message.id,
            'text': message.text,
            'sender': message.sender.id,
            'sender_name': message.sender.get_full_name() or message.sender.username,
            'timestamp': message.timestamp.isoformat()
        })
    
    return JsonResponse({'messages': messages})