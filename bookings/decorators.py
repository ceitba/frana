from functools import wraps

from django.shortcuts import redirect

REDIRECT_URL = 'bookings:index'


def anonymous_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_anonymous():
            return redirect(REDIRECT_URL)
        return view_func(request, *args, **kwargs)
    return _wrapped_view
