def navbar_context(request):
    user_id = None
    if request.user.is_authenticated:
        user_id = request.user.id
    return {'user_id': user_id}

    
