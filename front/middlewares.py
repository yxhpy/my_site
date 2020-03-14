from django.contrib.auth.models import User


def front_user_middleware(get_response):
    def middleware(request):
        user_id = request.session.get('user_id')
        user = User.objects.filter(id=user_id).first()
        if user:
            username = user
        else:
            username = None
        request.username = username
        request.user_id = user_id
        request.user = user
        response = get_response(request)
        return response

    return middleware
