from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework import status
import requests
from django.contrib import messages
from django.shortcuts import get_object_or_404
import json
from .models import Employee
from .serializers import EmpSerializers,LoginSerializers
from django.contrib.auth import authenticate
# Create your views here.

# JWT Configration
# from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser


# @api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])

@api_view(['POST'])
def verify_token(request):
    token=request.COOKIES.get('jwt')
    try:
        # Decode the token using UntypedToken
        UntypedToken(token)
    except (InvalidToken, TokenError) as e:
        return Response({"detail": "Token is invalid or expired"}, status=401)

    return Response({"detail": "Token is valid"}, status=200)

def index(request):    
    try:
        authentication_classes = [JWTAuthentication]
        jwt_token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        print("FFFFFFFFFFFFFFFFFFFFFF",jwt_token)
    except Exception as e:
        print("index error",e)  
    return render(request, 'index.html')


def registration(request):
    # Extract form data from request.POST
    if request.method == 'POST':
        first_name = request.POST['Fname']
        last_name = request.POST['Lname']
        Date_of_birth = request.POST['Dob']
        email = request.POST['Mail']
        password = request.POST['Password']
        Phone_Number = request.POST['MobileNumber']
        Gender = request.POST['Gender']
        User_type = request.POST['User_Type']
        
        print("---------->",first_name,last_name,Date_of_birth,User_type)
        # Construct data dictionary
        data = {
            'First_Name': first_name,
            'Last_Name': last_name,
            'Email': email,
            'Password': password,
            'Phone_Number': Phone_Number,
            'Gender': Gender
        }
        
        # Make a POST request to the API endpoint
        BASEURL = "http://127.0.0.1:8000/"
        ENDPOINT ='register_api/'
        response = requests.post(BASEURL + ENDPOINT, json.dumps(data),headers=headers)
        print("------------------------",response)
        if response.status_code == 201:
            messages.success(request, 'Registration successful!')
            return redirect('login')  # Redirect to a success page.
        else:
            print('Registration failed:', response.json())
            messages.error(request, 'Registration failed: ')
    return render(request, 'signup.html')

@api_view(['POST'])
def employee_list(request):
    data = request.data
    print(data)
    print(type(request.data))
    if request.method == "POST":
        try:
            emp_info=EmpSerializers(data=request.data)
        except Exception as e:
            print("Might be an error in Serializer",e)
        try:
            if emp_info.is_valid():
                emp_info.save()
                return Response(emp_info.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Might be an error in Data validation",e)
        return Response(emp_info.errors)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def login(request):
    if request.method == "POST":
        email = request.POST['Mail']
        password = request.POST['Password']
        data = {
            "Email": email,
            "Password":password
        }
        print("---------------*******************************------------->>>>",type(data),email,password)
        headers = {'Content-Type': 'application/json'}
        BASE_URL = "http://127.0.0.1:8000/"
        ENDPOINT = 'login_api/'
        res=requests.post(BASE_URL + ENDPOINT, json.dumps(data),headers=headers)
        print("========================>",res)
        if res.status_code == 200:
            try:
                response_data = res.json()
                print("================>",response_data)
                import jwt
                # access_token_str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE3MDU1NTE0LCJpYXQiOjE3MTcwNTUyMTQsImp0aSI6IjMxOTBmZGQ3ZDRmMzQ3N2JhNzAwNDI0MWI1NjZkM2IxIiwidXNlcl9pZCI6Nn0.of6yxKAstIMdkaO9NpCXpAl54gZw0A6nBeOemO6v6b8'
                access_token = response_data.get('access')
                # decoded_payload=jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
                # print("*******************////////////////////////",decoded_payload)
                # decoded_payload=access_token.payload
                # token_type = access_token['token_type']
                # # typesss = access_token['user_id']
                # typesss = access_token.get('emp')
                # exp = access_token['exp']
                # print("access_token",decoded_payload)

                    
                if 'message' in response_data and response_data['message'] == 'Login successful!':
                    # Login successful, redirect to desired page (e.g., 'index')
                    print("------------>>>>>>>>>>>>>",access_token)
                    payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
                    print("Payload:", payload)
                    response = HttpResponseRedirect(reverse('index'))
                    response.set_cookie('jwt', access_token, httponly=True)
                    return response
                else:
                    # Handle unexpected response content
                    messages.error(request, 'Login failed: Unexpected response from server.')
            except json.JSONDecodeError as e:
                print("JSON Decode Error:", e)
                messages.error(request, "Server returned invalid JSON.")
                # print("Response text:", res.text)
                # messages.error(request, "Server returned invalid JSON.")
            except Exception as e:
                print("Unexpected Error:", e)
                messages.error(request, 'Login failed: An unexpected error occurred.')
        else:
            # Handle unsuccessful login (non-200 status code)
            try:
                response_data = res.json()
                if 'error' in response_data:
                    messages.error(request, 'Login failed: ' + response_data['error'])
                else:
                    messages.error(request, 'Login failed: ' + str(res.status_code))  # Include status code
                    return render(request, 'login.html', {"error": "Login failed"})  # Render login template with error
            except json.JSONDecodeError as e:
                print("JSON Decode Error:", e)
                messages.error(request, "Server returned invalid JSON.")
            except Exception as e:
                print("Unexpected Error:", e)
                messages.error(request, 'Login failed: An unexpected error occurred.')
    else:
        return render(request, 'login.html', {"error": "Might be an issue"})


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def login_api(request):
    print("data of request ****************",type(request.data))
    try:
        serializer = LoginSerializers(data=request.data)
        try:
            if serializer.is_valid():
                emp=serializer.validated_data['employee']
                refresh = RefreshToken.for_user(emp)
                print(refresh)
                return Response({
                    'emp':str(emp),
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    "message": "Login successful!"
                }, status=status.HTTP_200_OK)
                
                # print("==================>",serializer.data)
                # return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
            
        except Exception as e:
            # Handle other errors appropriately
            return Response({"error": "An error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        print(e)
        return Response(serializer.errors)

from django.conf import settings
import jwt

def Profile(request):
    token=request.COOKIES.get('jwt')
    print('==========>111211111122222222221!!!!!!!!!!!!>>',token)
    try:
        # Decode the token using UntypedToken
        token_verify=UntypedToken(token)
        if token_verify:
            # Employee.objects.filter(Email=Email)   
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            print("Payload:", payload) 
        
        if request.method == 'POST':
            first_name = request.POST['Fname']
            last_name = request.POST['Lname']
            Phone_Number = request.POST['MobileNumber']
            Email = request.POST['Email']
            Gender = request.POST['Gender']
            print("===>",first_name,last_name,Gender,Phone_Number,Email)
            data = {
                'First_Name': first_name,
                'Last_Name': last_name,
                'Phone_Number': Phone_Number,
                'Gender': Gender
            }
            print("]]]",data)
            
            
        # BASEURL = "http://127.0.0.1:8000/"
        # ENDPOINT ='get_profile_details/'
                
        # headers = {'Content-Type': 'application/json',
        #             'Authorization': f'Bearer {token}',
        #             'Email':Email}
        # response = requests.get(BASEURL + ENDPOINT,headers=headers)
    
            try:
                BASEURL = "http://127.0.0.1:8000/"
                ENDPOINT ='profile_api/'
                
                headers = {'Content-Type': 'application/json'}
                response = requests.post(BASEURL + ENDPOINT, json.dumps(data),headers=headers)
            except Exception as e:
                print("Showing Error",e)
            print("------------------------",response)
            # user_info=Employee.objects.filter()
        return render(request,'profile.html')
    except (InvalidToken, TokenError) as e:
        print("ERROR",e)
        return redirect('login')
    # return Response({"detail": "Token is valid"}, status=200)



@api_view(['GET'])
def get_profile_details(request):
    pass
    

@api_view(['POST'])
def profile_api(request):
    data = request.data
    print("------------------------------------>",data)
    print(type(request.data))