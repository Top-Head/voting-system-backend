import random
import string
from api.models import Voter
from rest_framework import status
from django.utils import timezone
from django.core.mail import EmailMessage
from api.serializers import VoterSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password


@api_view(['POST'])
def register_voter(request):
    data = request.data.copy()
    if not data.get('email') or not data.get('password') or not data.get('name'):
        return Response({"error": "Name, email and password required"}, status=status.HTTP_400_BAD_REQUEST)

    if Voter.objects.filter(email=data['email']).exists():
        return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

    data['password'] = make_password(data['password'])
    serializer = VoterSerializer(data=data)
    
    if serializer.is_valid():
        voter = serializer.save()
        
        code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        voter.verification_code = code
        voter.code_generated_at = timezone.now()
        voter.save()
        
        html = render_to_string("email_verify.html", {"code": code})
        subject = "Verify Email"
        from_email = "omarscode007@gmail.com"
        to = voter.email
        msg = EmailMessage(subject, html, from_email, [to])
        msg.content_subtype = 'html'
        msg.send()
        
        return Response({
            "message": "Voter registered successfully! Please check your email for verification code.",
            "email": voter.email,
            "redirect_to_verify": True
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verify_email(request):
    email = request.data.get('email')
    code = request.data.get('code')
    
    if not email or not code:
        return Response({"error": "Email and code are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        voter = Voter.objects.get(email=email)
    except Voter.DoesNotExist:
        return Response({"error": "Email not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if voter.verification_code != code:
        return Response({"error": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)
    
    if voter.code_generated_at and (timezone.now() - voter.code_generated_at).total_seconds() > 7200:
        return Response({"error": "Verification code has expired"}, status=status.HTTP_400_BAD_REQUEST)
    
    voter.is_active = True
    voter.verification_code = None 
    voter.code_generated_at = None
    voter.save()
    
    return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)

@api_view(['POST'])  
def voter_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"error": "Email and password required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        voter = Voter.objects.get(email=email)
    except Voter.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    if voter.is_active == False:
        return Response({"error": "Your account is inative, verify your account first"}, status=status.HTTP_401_UNAUTHORIZED)

    if not check_password(password, voter.password):
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(voter)
    refresh['email'] = voter.email
    access_token = refresh.access_token
    access_token['email'] = voter.email

    return Response({
        "refresh": str(refresh),
        "token": str(access_token),
        "email": voter.email
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def voter_refresh_token(request):
    refresh_token = request.data.get("refresh")

    if not refresh_token:
        return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh = RefreshToken(refresh_token)
        access_token = refresh.access_token
        return Response({
            "access": str(access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Invalid or expired refresh token: {e}"}, status=status.HTTP_401_UNAUTHORIZED)
