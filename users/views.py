from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, email=email, password=password)

    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    


@csrf_exempt
@login_required
def user_details(request):
    if request.user.is_authenticated:
        user = request.user
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'referral_code':user.referral_code
            
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Authentication required'}, status=401)


@csrf_exempt
@login_required
def user_referrals(request):
    if request.user.is_authenticated:
      current_user = request.user
      referrals = User.objects.filter(referral_code=current_user.referral_code)
      data = {
            'id':referrals.id,
            'username':referrals.username,
            'email':referrals.email,
            'referral_code':referrals.referral_code,
            'points':referrals.points    
        }
      return JsonResponse(data)
    else:
      return JsonResponse({'error': 'Authentication required'}, status=401)