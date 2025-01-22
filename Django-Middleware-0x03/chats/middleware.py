from datetime import datetime, timedelta
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        with open("requests.log", "a") as log_file:
            log_file.write(log_entry)
        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        if now.hour < 18 or now.hour >= 21:
            return HttpResponseForbidden("Access to the chat is restricted during this time.")
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.user_messages = {}

    def __call__(self, request):
        if request.method == "POST":
            ip = request.META.get("REMOTE_ADDR")
            now = datetime.now()

            if ip not in self.user_messages:
                self.user_messages[ip] = []
            self.user_messages[ip] = [t for t in self.user_messages[ip] if now - t < timedelta(minutes=1)]

            if len(self.user_messages[ip]) >= 5:
                return HttpResponseForbidden("Message limit exceeded. Please wait before sending more messages.")

            self.user_messages[ip].append(now)
        return self.get_response(request)

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated or request.user.role not in ["admin", "moderator"]:
            return HttpResponseForbidden("You do not have permission to perform this action.")
        return self.get_response(request)
