from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework.views import APIView
from .models import ApiKey, User, UserProfile
from .serializers import UserProfileSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
import random
import string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.renderers import JSONRenderer
from django.utils import timezone
from .models import PasswordReset
from .serializers import PasswordResetSerializer
import jwt
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail
from django.utils.encoding import force_str

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import TokenError, UntypedToken
from rest_framework_simplejwt.state import token_backend




class TestView(APIView):
    @swagger_auto_schema(
        operation_description="This endpoint checks the connection and returns a message.",
        responses={
            200: openapi.Response(
                description="Connection successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
        }
    )
    def get(self, request):
        status_code = status.HTTP_200_OK
        message = "Connection was successful"

        return Response({"message": message}, status=status_code)



class SignupView(APIView):

    @swagger_auto_schema(
        
        operation_description="This endpoint is for users to sign up",

        manual_parameters=[
            openapi.Parameter('first_name', openapi.IN_QUERY, description="First name of the user", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('last_name', openapi.IN_QUERY, description="Last name of the user", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('email', openapi.IN_QUERY, description="Email address of the user", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('password', openapi.IN_QUERY, description="User's Password", type=openapi.TYPE_STRING, required=True),
        ],

        responses={
            201: openapi.Response(
                description="Account created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                        'access': openapi.Schema(type=openapi.TYPE_STRING),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                ),
            ),
        }
    )
    

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Generate a 10-character alphanumeric account_id
            account_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            user = serializer.save(account_id=account_id)
            refresh = RefreshToken.for_user(user)
            res = {
                'status': status.HTTP_201_CREATED,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'account_id': account_id,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Account created successfully'
            }
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
            
        operation_description="This endpoint is for users to login",

        manual_parameters=[
            openapi.Parameter('email', openapi.IN_QUERY, description="Email address of the user", type=openapi.TYPE_STRING),
            openapi.Parameter('password', openapi.IN_QUERY, description="User's Password", type=openapi.TYPE_STRING),
        ],

        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                        'access': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                ),
            ),
            404: openapi.Response(description="Invalid email or password"),
        },
    )

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_404_NOT_FOUND)
        
        if not user.check_password(password):
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_404_NOT_FOUND)

        refresh = RefreshToken.for_user(user)

        res = {
                'status': status.HTTP_200_OK,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }

        return Response(res, status=status.HTTP_200_OK)


class RequestPasswordReset(APIView):

    @swagger_auto_schema(
        operation_description="Submit a request for a password reset link by providing an email address.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="Email address for password reset"),
            },
            required=['email'],
        ),
        responses={
            200: openapi.Response(description="Password reset link sent successfully"),
            400: openapi.Response(description="Invalid email (User does not exist)"),
        }
    )

    def post(self, request):
        data = request.data
        email = data['email']
        
        try:
            user = User.objects.get(email=email)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_url = f'https://softrobe-server.onrender.com/api/v1/auth/reset-password/{uid}/{token}/'

            send_mail(
                'Password Reset Request', 
                f'Click here to reset your password: {reset_url}',
                'no-reply@email.princewilldev.com',
                [user.email],
                fail_silently=False
            )

            return Response({'message': 'Password resent link sent successfully'})
        
        except User.DoesNotExist:
            return Response({'error':'Invalid email'}, status=400)


class PasswordResetConfirmView(APIView):

    @swagger_auto_schema(
        operation_description="Confirm a password reset by providing a valid reset link.",
        manual_parameters=[
            openapi.Parameter('uidb64', openapi.IN_PATH, description="User ID encoded in base64", type=openapi.TYPE_STRING),
            openapi.Parameter('token', openapi.IN_PATH, description="Token for password reset", type=openapi.TYPE_STRING),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, description="New password for the user"),
            },
            required=['new_password'],
        ),
        responses={
            200: openapi.Response(description="Password reset success"),
            400: openapi.Response(description="Invalid reset link"),
        }
    )


    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

        except Exception as e:
            user = None
        
        if user and default_token_generator.check_token(user, token):
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password reset success'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid reset link'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="This endpoint displays the user's profile.",
        responses={
            200: openapi.Response(
                description="OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                        'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                        'address': openapi.Schema(type=openapi.TYPE_STRING),
                        'addressline2': openapi.Schema(type=openapi.TYPE_STRING),
                        'city_or_town': openapi.Schema(type=openapi.TYPE_STRING),
                        'state_province_region': openapi.Schema(type=openapi.TYPE_STRING),
                        'zip_code': openapi.Schema(type=openapi.TYPE_STRING),
                        'age_range': openapi.Schema(type=openapi.TYPE_STRING),
                        'profession': openapi.Schema(type=openapi.TYPE_STRING),
                        'dress_code': openapi.Schema(type=openapi.TYPE_STRING),
                        'dress_code_description': openapi.Schema(type=openapi.TYPE_STRING),
                        'upcoming_events': openapi.Schema(type=openapi.TYPE_STRING),
                        'upcoming_events_description': openapi.Schema(type=openapi.TYPE_STRING),
                        'activity': openapi.Schema(type=openapi.TYPE_STRING),
                        'activity_items': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                        'activity_frequency': openapi.Schema(type=openapi.TYPE_STRING),
                        'sports_fan': openapi.Schema(type=openapi.TYPE_STRING),
                        'sports_team': openapi.Schema(type=openapi.TYPE_STRING),
                        'description_items': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                        'outdoor_activities': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                        'fashion_goals': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                        'attention_points': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                        'image_base64': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                    },
                ),
            ),
        },
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT access token", type=openapi.TYPE_STRING),
        ]
    )

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        try:
            valid_data = token_backend.decode(token, verify=False)
            user = User.objects.get(id=valid_data['user_id'])
        except (TokenError, User.DoesNotExist) as e:
            raise AuthenticationFailed('Invalid token')

        return Response(UserSerializer(user).data)


class UserProfileUpdate(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="This endpoint updates the user's profile.",
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT access token", type=openapi.TYPE_STRING),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                'address': openapi.Schema(type=openapi.TYPE_STRING),
                'addressline2': openapi.Schema(type=openapi.TYPE_STRING),
                'city_or_town': openapi.Schema(type=openapi.TYPE_STRING),
                'state_province_region': openapi.Schema(type=openapi.TYPE_STRING),
                'zip_code': openapi.Schema(type=openapi.TYPE_STRING),
                'age_range': openapi.Schema(type=openapi.TYPE_STRING),
                'profession': openapi.Schema(type=openapi.TYPE_STRING),
                'dress_code': openapi.Schema(type=openapi.TYPE_STRING),
                'dress_code_description': openapi.Schema(type=openapi.TYPE_STRING),
                'upcoming_events': openapi.Schema(type=openapi.TYPE_STRING),
                'upcoming_events_description': openapi.Schema(type=openapi.TYPE_STRING),
                'activity': openapi.Schema(type=openapi.TYPE_STRING),
                'activity_description': openapi.Schema(type=openapi.TYPE_STRING),
                'activity_frequency': openapi.Schema(type=openapi.TYPE_STRING),
                'sports_fan': openapi.Schema(type=openapi.TYPE_STRING),
                'sports_team': openapi.Schema(type=openapi.TYPE_STRING),
                'description_items': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                'activity_items': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                'fashion_goals': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                'attention_points': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                'image_base64': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
            },
        ),
        responses={
            200: openapi.Response(description="Profile updated successfully"),
            400: openapi.Response(description="Invalid data"),
        }
    )

    def patch(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        try:
            valid_data = token_backend.decode(token, verify=False)
            user = User.objects.get(id=valid_data['user_id'])
        except (TokenError, User.DoesNotExist) as e:
            raise AuthenticationFailed('Invalid token')

        userprofile = UserProfile.objects.get(user=user)
        serializer = UserProfileSerializer(userprofile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FullProfileView(APIView):

    @swagger_auto_schema(
        operation_description="Get a user's full profile by providing a valid API key.",
        manual_parameters=[
            openapi.Parameter('X-API-KEY', openapi.IN_HEADER, description="Enter Provisioned API Key", type=openapi.TYPE_STRING),
        ],
        responses={
            200: openapi.Response(description="User profile retrieved successfully"),
            400: openapi.Response(description="API key required"),
            403: openapi.Response(description="Invalid API key"),
        }
    )

    def get(self, request, account_id):
        api_key = request.headers.get('X-API-KEY')
        if not api_key:
            return Response({"message": "API key required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the API key exists. If it does, get the user's full profile.
        if ApiKey.objects.filter(api_key=api_key).exists():
            user = get_object_or_404(User, account_id=account_id)
            userprofile = UserProfile.objects.get(user=user)
            serializer = UserProfileSerializer(userprofile)
            return Response(serializer.data)
        else:
            return Response({"message": "Invalid API key"}, status=status.HTTP_403_FORBIDDEN)
        


class RetriveUserProfile(APIView):

    @swagger_auto_schema(
        operation_description="Get a user's full profile.",
        responses={
            200: openapi.Response(description="User profile retrieved successfully"),
        }
    )

    def get(self, request, account_id):
        # No need to check for API key anymore
        user = get_object_or_404(User, account_id=account_id)
        userprofile = UserProfile.objects.get(user=user)
        serializer = UserProfileSerializer(userprofile)
        return Response(serializer.data)
    
    
    

class ListUsers(APIView):

    @swagger_auto_schema(
        operation_description="Get a list of all registered users.",
        responses={
            200: openapi.Response(description="List retrieved successfully"),
        }
    )


    def get(self, request):
        users = User.objects.all()
        data = []
        for user in users:
            data.append({
                'account_id': user.account_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'details-link': f'https://softrobe-server.onrender.com/api/v1/auth/user/details/{user.account_id}/',
            })
        return Response(data)