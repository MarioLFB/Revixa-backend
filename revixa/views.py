from django.http import JsonResponse

def home(request):
    return JsonResponse({"status": 200, "message": "Hello, welcome to Revixa Django REST Framework API"})
