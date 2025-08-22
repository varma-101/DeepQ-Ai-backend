from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import Response
from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

# Create your views here.

@api_view(["GET"])
def sample_data(request):
    return Response("Hello")

@csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        username = data.get("username")
        password = data.get("password")
        email = data.get("email", "")

        # validate inputs
        if not username or not password:
            return JsonResponse({"error": "Username and password are required"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        return JsonResponse({"message": "User created successfully"}, status=201)

@csrf_exempt
def api_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({"error": "Username and password are required"}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful"})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def worldbank_data(request):
    url = "http://api.worldbank.org/v2/country/IN/indicator/NY.GDP.MKTP.CD?format=json"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    if isinstance(data, list) and len(data) > 1:
        return JsonResponse(data[1], safe=False) 
    return JsonResponse({"message": "No data found"})
