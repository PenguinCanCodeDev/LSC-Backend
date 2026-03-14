from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import status


from .models import User, UserTypes
from .serializers import UserSerializer
from .utils import is_valid_email
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method="get",
    tags=["General"],
    operation_summary="API Home",
    operation_description="""
    Basic API health check endpoint.

    Returns a simple message indicating that the API is running and developed
    by the Penguins Can Code Team.

    **Authentication:** Not required.
    """,
    responses={
        200: openapi.Response(
            description="API is running",
            examples={
                "application/json": "Developed by Penguins Can Code Team."
            }
        )
    }
)
@api_view(['GET'])
def home(request):

    return Response("Developed by Penguins Can Code Team.")


@swagger_auto_schema(
    method="get",
    tags=["Users"],
    operation_summary="Get authenticated user information",
    operation_description="""
    Returns the profile details of the currently authenticated user.

    **Authentication Required:** Yes (JWT Access Token)

    The access token should be included in the request header:
```
    Authorization: Bearer <access_token>
```

    Returns basic user information such as email, campus, department and
    matriculation number.
    """,
    responses={
        200: openapi.Response(
            description="User information retrieved successfully",
            examples={
                "application/json": {
                    "id": 1,
                    "email": "student@university.edu",
                    "campus": "Main Campus",
                    "faculty": "Engineering",
                    "department": "Computer Science",
                    "matriculation_number": "CSC2024001",
                    "user_type": "lsc"
                }
            }
        ),
        401: openapi.Response(
            description="Authentication credentials missing or invalid"
        )
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):

    user = request.user

    user_serializer = UserSerializer(user)

    return Response(user_serializer.data)

@swagger_auto_schema(
    method="post",
    tags=["Auth"],
    operation_summary="Register a new student account",
    operation_description="""
    Creates a new student account.

    **Required Fields:**

    - Email (must be valid and unique)
    - Password (minimum 5 characters)
    - First name
    - Last name
    - Campus
    - Faculty
    - Department
    - Matriculation number (must be unique)
    - User type (l300 or lsc)

    **Notes for Frontend:**

    - Email must be a valid email format.
    - Matriculation number must be unique.
    - Password must be at least **5 characters long**.
    - On successful registration, the API automatically returns **JWT access and refresh tokens**.
    - These tokens should be stored securely and used for authenticated requests.

    **Authentication:** Not required.
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=[
            "email",
            "password",
            "campus",
            "faculty",
            "department",
            "matriculation_number",
            "first_name",
            "last_name",
            "user_type"
        ],
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_EMAIL,
                description="Student's email address"
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_PASSWORD,
                description="Password (minimum 5 characters)"
            ),
            "first_name": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Student's first name"
            ),
            "last_name": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Student's last name"
            ),
            "campus": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Student's campus"
            ),
            "faculty": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Student's faculty"
            ),
            "department": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Student's department"
            ),
            "matriculation_number": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Unique matriculation number"
            ),
            "user_type": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="User type (l300 or lsc)",
                enum=["l300", "lsc"]
            ),
        },
        example={
            "email": "student@university.edu",
            "password": "securepass123",
            "first_name": "John",
            "last_name": "Doe",
            "campus": "Main Campus",
            "faculty": "Engineering",
            "department": "Computer Science",
            "matriculation_number": "CSC2024001",
            "user_type": "l300"
        }
    ),
    responses={
        200: openapi.Response(
            description="Account created successfully",
            examples={
                "application/json": {
                    "status": True,
                    "message": "Account created successfully",
                    "user": {
                        "id": 1,
                        "email": "student@university.edu",
                        "campus": "Main Campus",
                        "faculty": "Engineering",
                        "department": "Computer Science",
                        "matriculation_number": "CSC2024001",
                        "user_type": "l300"
                    },
                    "tokens": {
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                    }
                }
            }
        ),
        400: openapi.Response(
            description="Validation error",
            examples={
                "application/json": {
                    "status": False,
                    "message": "All fields are required"
                }
            }
        )
    }
)
@api_view(['POST'])
def register_user(request):

    email = request.data.get('email')
    password = request.data.get('password')
    campus = request.data.get('campus')
    faculty = request.data.get('faculty')
    department = request.data.get('department')
    matriculation_number = request.data.get('matriculation_number')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    user_type = request.data.get('user_type', 'l300')
    
    # validate data
    
    if not all([
        email, password, campus, faculty,
        department, matriculation_number,
        first_name, last_name
    ]):
        return Response({
            'status': False,
            'message': 'All fields are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if not is_valid_email(email):
        return Response({
            'status': False,
            'message': 'Invalid email provided'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(matriculation_number=matriculation_number).exists():
        return Response({
            'status': False,
            'message': 'Matric number already in use'
        }, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({
            'status': False,
            'message': 'Email already in use'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if len(password) < 5:
        return Response({
            'status': False,
            'message': 'Password must be at least 5 characters'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if user_type not in ['l300', 'lsc']:
        return Response({
            'status': False,
            'message': 'user_type must be either l300 or lsc'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    new_user = User.objects.create_user(
        email = email,
        first_name = first_name,
        last_name = last_name,
        campus = campus,
        faculty = faculty,
        department = department,
        matriculation_number = matriculation_number,
        password = password,
        user_type = user_type
    )
    serializer = UserSerializer(new_user)

    return Response({
        'status': True,
        'message': 'Account created successfully',
        'user': serializer.data,
        'tokens': new_user.auth_tokens()  
    })

@swagger_auto_schema(
    method="post",
    tags=["Auth"],
    operation_summary="Login user",
    operation_description="""
    Authenticates a user using either **email** or **matriculation number**.

    **Login Options:**

    1️⃣ Email + Password  
    2️⃣ Matriculation Number + Password

    At least **one identifier (email OR matric number)** must be provided.

    **Notes for Frontend:**

    - Email must be a valid email format if provided.
    - Password must match the user's stored password.
    - On successful login, **JWT access and refresh tokens** are returned.
    - Use the access token for authenticated API requests.

    **Authentication:** Not required.
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["password"],
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_EMAIL,
                description="User's registered email address (optional if matric_number provided)"
            ),
            "matric_number": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="User's matriculation number (optional if email provided)"
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_PASSWORD,
                description="User's password"
            )
        },
        example={
            "email": "student@university.edu",
            "password": "securepass123"
        }
    ),
    responses={
        200: openapi.Response(
            description="Login successful",
            examples={
                "application/json": {
                    "status": True,
                    "message": "Login successful",
                    "data": {
                        "user": {
                            "id": 1,
                            "email": "student@university.edu",
                            "campus": "Main Campus",
                            "faculty": "Engineering",
                            "department": "Computer Science",
                            "matriculation_number": "CSC2024001"
                        },
                        "tokens": {
                            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                        }
                    }
                }
            }
        ),
        400: openapi.Response(
            description="Missing login credentials",
            examples={
                "application/json": {
                    "status": False,
                    "message": "Email or matric number and password are required."
                }
            }
        ),
        401: openapi.Response(
            description="Invalid credentials",
            examples={
                "application/json": {
                    "status": False,
                    "message": "Invalid login credentials."
                }
            }
        ),
        404: openapi.Response(
            description="User not found"
        )
    }
)
@api_view(['POST'])
def login_user(request):

    email = request.data.get('email')
    matric_number = request.data.get('matric_number')
    password = request.data.get('password')

    if not ((email or matric_number) and password):
        return Response({
            "status": False,
            "message": "Email or matric number and password are required."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if email:
        if not is_valid_email(email):
            return Response({
                'status': False,
                'message': 'Invalid email provided'
            }, status=status.HTTP_400_BAD_REQUEST)
    
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'status': False,
                'message': 'No user with this email exists'
            }, status=status.HTTP_404_NOT_FOUND)
        
    if matric_number:
        try:
            user = User.objects.get(matriculation_number=matric_number)
        except User.DoesNotExist:
            return Response({
                'status': False,
                'message': 'No user with this matric number'
            }, status=status.HTTP_404_NOT_FOUND)
        
    if user.check_password(password):
        
        return Response({
            'status': True,
            'message': 'Login successful',
            'data': {
                "user": UserSerializer(user).data,
                "tokens": user.auth_tokens()
            }
        }, status=status.HTTP_200_OK)
    
    return Response({
        'status': False,
        'message': 'Invalid login credentials.',
    }, status=status.HTTP_401_UNAUTHORIZED)

@swagger_auto_schema(
    method="post",
    request_body=TokenRefreshSerializer,
    responses={
        200: openapi.Response(
            description="Token refresh successful",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, description="Always 'success' when refresh is successful"),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description="Human-readable message"),
                    'data': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'access': openapi.Schema(type=openapi.TYPE_STRING, description='Newly issued access token'),
                            'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Original refresh token (still valid until expiry)')
                        }
                    )
                },
                example={
                    "status": True,
                    "message": "Token refreshed successfully",
                    "data": {
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                    }
                }
            )
        ),
        400: openapi.Response(
            description="Bad Request - Invalid request format or missing fields",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "status": openapi.Schema(type=openapi.TYPE_STRING, description="Always 'error'"),
                    "message": openapi.Schema(type=openapi.TYPE_STRING, description="Explanation of what went wrong")
                }
            ),
            example={
                "status": False,
                "message": "The 'refresh' field is required."
            }
        ),
        401: openapi.Response(
            description="Unauthorized - Invalid, expired, or blacklisted refresh token",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "status": openapi.Schema(type=openapi.TYPE_STRING, description="Always 'error'"),
                    "message": openapi.Schema(type=openapi.TYPE_STRING, description="Reason token could not be used")
                }
            ),
            example={
                "status": False,
                "message": "Token is invalid or has expired"
            }
        ),
    },
    operation_description="""
    **Purpose:**  
    Use this endpoint to obtain a new **access token** by providing a valid **refresh token**.

    ---
    **Token lifetimes in this project:**
    - **Access token:** 1 day
    - **Refresh token:** 30 days

    ---
    **Common Error Scenarios:**
    - **Missing refresh token** → 400 with `{ "status": False, "message": "The 'refresh' field is required." }`
    - **Expired/blacklisted token** → 401 with `{ "status": False, "message": "Token is invalid or has expired" }`
    - **Malformed request** (e.g., wrong field name) → 400

    ---
    **Frontend Tips:**
    - Store `access` tokens in memory (short-lived).
    - Store `refresh` tokens securely (e.g., HTTP-only cookies or secure storage).
    - If you get a 401 from this endpoint, redirect to login.
    """,
    operation_summary="Refresh access token",
    tags=["Auth"]
)
@api_view(["POST"])
def refresh_token(request):
    serializer = TokenRefreshSerializer(data=request.data)

    try:
        serializer.is_valid(raise_exception=True)
        return Response({
            "status": True,
            "message": "Token refreshed successfully",
            "data": serializer.validated_data
        }, status=status.HTTP_200_OK)

    except (TokenError, InvalidToken):
        return Response({
            "status": False,
            "message": "Token is invalid or has expired"
        }, status=status.HTTP_401_UNAUTHORIZED)

    except Exception:
        return Response({
            "status": False,
            "message": "An unexpected error occurred"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'refresh': openapi.Schema(
                type=openapi.TYPE_STRING, 
                description='Refresh token of the current session that needs to be blacklisted.'
            ),
        },
        required=['refresh'],
        example={
            'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
        },
    ),
    responses={
        204: openapi.Response(
            description="Successfully logged out.",
            examples={
                'application/json': {
                    'message': 'Successfully logged out.'
                }
            }
        ),
        400: openapi.Response(
            description="Bad Request",
            examples={
                'application/json': {
                    'error': 'Refresh token is required.'
                }
            }
        ),
    },
    operation_description=(
        "Logs out the current user by invalidating the provided refresh token. This action blacklists the refresh token, "
        "ensuring that it cannot be used to obtain new access tokens in the future. The refresh token must be included "
        "in the request body. If the token is missing or invalid, a 400 Bad Request error will be returned."
    ),
    operation_summary="Logout a user",
    tags=["Auth"]
)
@api_view(['POST'])
def logout_user(request):
    
    try:
        refresh_token = request.data.get("refresh")
        if refresh_token is None:
            return Response({
                "error": "Refresh token is required."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Blacklist the refresh token to prevent further use
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        return Response({
            "status": True,
            "message": "Successfully logged out."
            }, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({
            "status": False,
            "error": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='patch',
    operation_summary="Set user type",
    operation_description="Allows an authenticated user to set their user type.",
    tags=["Users"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['user_type'],
        properties={
            'user_type': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Type of user",
                enum=['l300', 'lsc']
            )
        }
    ),
    responses={
        200: openapi.Response(
            description="User type set successfully",
            examples={
                "application/json": {
                    "status": True,
                    "message": "User type set successfully"
                }
            }
        ),
        400: openapi.Response(
            description="Invalid input",
            examples={
                "application/json": {
                    "status": False,
                    "message": "user_type is required"
                }
            }
        )
    }
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def set_user_type(request):

    user = request.user

    user_type = request.data.get('user_type')
    if not user_type:
        return Response({
            "status": False,
            "message": "user_type is required"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if not user_type in list(UserTypes.values):
        return Response({
            "status": False,
            "message": "user_type can either be l300 or lsc"
        }, status=status.HTTP_400_BAD_REQUEST)

    user.user_type = user_type
    user.save(update_fields=['user_type'])

    return Response({
        "status": True,
        "message": "User type set successfully"
    }, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='patch',
    operation_summary="Edit user profile",
    operation_description="""
    Allows an authenticated user to update their profile information.

    **All fields are optional** — only send the fields you want to update.

    **Editable Fields:**
    - **first_name** → Student's first name
    - **last_name** → Student's last name
    - **department** → Student's department
    - **faculty** → Student's faculty
    - **campus** → Student's campus
    - **level** → Student's level
    - **matriculation_number** → Must be unique if changed
    - **user_type** → l300 or lsc

    **Authentication Required:** Yes (JWT Access Token)
    """,
    tags=["Users"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "first_name": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Student's first name"
            ),
            "last_name": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Student's last name"
            ),
            "department": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Student's department"
            ),
            "faculty": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Student's faculty"
            ),
            "campus": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Student's campus"
            ),
            "level": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Student's level"
            ),
            "matriculation_number": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Student's matriculation number (must be unique)"
            ),
            "user_type": openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=["l300", "lsc"],
                description="User type"
            ),
        },
        example={
            "department": "Computer Science",
            "faculty": "Computing",
            "campus": "Legacy",
            "user_type": "l300"
        }
    ),
    responses={
        200: openapi.Response(
            description="Profile updated successfully",
            examples={
                "application/json": {
                    "status": True,
                    "message": "Profile updated successfully",
                    "user": {
                        "id": 1,
                        "email": "student@university.edu",
                        "first_name": "John",
                        "last_name": "Doe",
                        "campus": "Legacy",
                        "faculty": "Computing",
                        "department": "Computer Science",
                        "matriculation_number": "SCN/CSC/230123",
                        "user_type": "l300"
                    }
                }
            }
        ),
        400: openapi.Response(
            description="Validation error",
            examples={
                "application/json": {
                    "status": False,
                    "message": "Matric number already in use by another account"
                }
            }
        ),
        401: openapi.Response(
            description="Authentication credentials missing or invalid"
        ),
    }
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_profile(request):

    user = request.user

    # Fields allowed to be updated
    allowed_fields = [
        'first_name', 'last_name', 'department',
        'faculty', 'campus', 'level', 'matriculation_number', 'user_type'
    ]

    # Validate user_type if provided
    user_type = request.data.get('user_type')
    if user_type and user_type not in list(UserTypes.values):
        return Response({
            'status': False,
            'message': 'user_type must be either l300 or lsc'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Validate matriculation_number uniqueness only if it is being changed
    new_matric = request.data.get('matriculation_number')
    if new_matric and new_matric != user.matriculation_number:
        if User.objects.filter(matriculation_number=new_matric).exists():
            return Response({
                'status': False,
                'message': 'Matric number already in use by another account'
            }, status=status.HTTP_400_BAD_REQUEST)

    # Apply only the fields that were sent in the request
    updated_fields = []
    for field in allowed_fields:
        value = request.data.get(field)
        if value is not None and str(value).strip():
            setattr(user, field, str(value).strip())
            updated_fields.append(field)

    if updated_fields:
        user.save(update_fields=updated_fields)

    serializer = UserSerializer(user)

    return Response({
        'status': True,
        'message': 'Profile updated successfully',
        'user': serializer.data
    }, status=status.HTTP_200_OK)