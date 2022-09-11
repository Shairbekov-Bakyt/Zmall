from chat.models import Chat

def get_messages_from_user(request):
    return Chat.objects.select_related('from_user', 'to_user', 'advert').filter(from_user=request.user)

def get_messages_to_user(request):
    return Chat.objects.select_related('from_user', 'to_user', 'advert').filter(to_user=request.user)

def get_messages_from_advert_id(request, pk):
    return Chat.objects.select_related('from_user', 'to_user', 'advert').filter(advert=pk).order_by('-date')
