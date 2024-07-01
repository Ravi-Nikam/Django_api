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
from .models import Employee,product
from .serializers import *
from django.contrib.auth import authenticate
# Create your views here.

# JWT Configration
# from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from django.contrib.auth import get_user_model


User = get_user_model()
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
        print("User=============>",request.user)
        # print("------------------------->>",request.session['user_email'])
        if request.session.get('user_email') and request.COOKIES.get('jwt'):
            return render(request,'index.html')
        else:
            request.session['user_email'] = str(request.user)
            try:
                refresh = RefreshToken.for_user(request.user)
                print(refresh)
                print(refresh.access_token)
                response = HttpResponseRedirect(reverse('index'))
                response.set_cookie('jwt',refresh.access_token, httponly=True)
                return response
            except Exception as e:
                print("Error in generating token",e)
            print("-------------------------@@@@@@@@@@@@@@>>>>>>>>>>",request.session['user_email'])
            return render(request,'index.html')
            # return HttpResponse("DONE")
            
            # authentication_classes = [JWTAuthentication]
            # jwt_token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            # print("FFFFFFFFFFFFFFFFFFFFFF",jwt_token)
    except Exception as e:
        print("user facing error===========>",e)            


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
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            "dob" : Date_of_birth,
            'password': password,
            'phone_number': Phone_Number,
            'gender': Gender
        }
        # Make a POST request to the API endpoint
        BASEURL = "http://localhost:8000/"
        ENDPOINT ='register_api/'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(BASEURL + ENDPOINT, json.dumps(data),headers=headers)
        print("------------------------",response.json())
        if response.status_code == 201:
            messages.success(request, 'Registration successful!')
            return redirect('login')  # Redirect to a success page.
        else:
            print('Registration failed:', response.json())
            messages.error(request, 'Registration failed: ')
    return render(request, 'signup.html')

@api_view(['POST'])
def employee_list(request):
    print("MIght be an error")
    data = request.data
    print("================>>",data)
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
        headers = {'Content-Type': 'application/json'}
        BASE_URL = "http://localhost:8000/"
        ENDPOINT = 'login_api/'
        res=requests.post(BASE_URL + ENDPOINT, json.dumps(data),headers=headers)
        print("=====>12222")
        print("********************************>",res)
        # Perform authentication (assuming email is used for authentication)
        print("==========>",res.json())
        data=res.json()
        print("****************========>",data['emp']['Email'])
        if res.status_code == 200:
            try:
                try:
                    session_mail = data['emp']['Email']
                    request.session['user_email']= session_mail
                    print("------------------------------------------->>>",request.session.get('user_email'))
                except Exception as e:
                    print("token stored",e)
                response_data = res.json()
                if 'message' in response_data and response_data['message'] == 'Login successful!':
                    # Login successful, redirect to desired page (e.g., 'index')
                    response = HttpResponseRedirect(reverse('index'))
                    print("Access token is printed",data['access'])
                    response.set_cookie('jwt',data['access'], httponly=True)
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
# @permission_classes([AllowAny])
def login_api(request):
    try:
        serializer = LoginSerializers(data=request.data)
        try:
            if serializer.is_valid():
                print("=======123=======>",serializer.data)
                emp=serializer.validated_data['employee']
                refresh = RefreshToken.for_user(emp)
                print(refresh)
                return Response({
                    'emp': serializer.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    "message": "Login successful!"
                }, status=status.HTTP_200_OK)
                
                print("==================>",serializer.data)
                return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
            
        except Exception as e:
            # Handle other errors appropriately
            return Response({"error": "An error occurred.","EROR":e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        print(e)
        return Response(serializer.errors)


def Profile(request):
    try:
        print("User=============>",request.user)
    except Exception as e:
        print("user facing error===========>",e)
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication] 
    print("session",request.session['user_email'])
    token=request.COOKIES.get('jwt')
    # Decode the token using UntypedToken
    token_verify=UntypedToken(token)
    print("here is my token 22",token_verify)
    print("here is my token",token)
    
    if request.method == 'POST':    
        print("Called")
        first_name = request.POST['Fname']
        last_name = request.POST['Lname']
        Phone_Number = request.POST['MobileNumber']
        # Email = request.POST['user_mail']
        Gender = request.POST['Gender']
        print("===>",first_name,last_name,Gender,Phone_Number)
        data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'phone_number': Phone_Number,
                    'gender': Gender,
                    'mail' : request.session.get('user_email')
                }
        if token_verify:
            try:
                BASEURL = "http://localhost:8000/"
                ENDPOINT ='Edit_profile_details/'
                print("TOKEN",token)
                # Headers for the request
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {token}'
                }
                resp = requests.post(BASEURL + ENDPOINT, json.dumps(data),headers=headers)
                print("Response status code:", resp.status_code)
            except jwt.ExpiredSignatureError:
                print("Token has expired")
            print("====>",data)
    try:
        if token_verify:
            try:
                BASEURL = "http://localhost:8000/"
                ENDPOINT ='get_profile_details/'
                # Headers for the request
                data = {
                    'mail' : request.session.get('user_email')
                }
                print(data.get('mail'))
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {token}'
                }
                resp = requests.post(BASEURL + ENDPOINT, json.dumps(data),headers=headers)
                print("Response status code:", resp.status_code)
                print("Response text:", resp.text)
            except jwt.ExpiredSignatureError:
                print("Token has expired")
            except jwt.InvalidTokenError:
                print("Invalid token")
            except Exception as e:
                print("An error occurred:", e)
            except Exception as e:
                print("might be an error",e)
                
            if resp.status_code == 200:
                print("DONE")
                # print("Response text:", resp.text)
                return render(request,'profile.html',{"res":resp.json()})
    except (InvalidToken, TokenError) as e:
        print("ERROR",e)
        return redirect('login')
    return render(request,'profile.html')


@api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
def get_profile_details(request):
    # return Response({"message": "Hello, world!"}, status=status.HTTP_200_OK)
    try:
        print("---->",request.data)
        print("***********",request.data['mail'])
        User_obj = User.objects.get(email=request.data['mail']) # Complex Data type Emp_obj is 
        print("XYZ",User_obj)
        Emp_serializer=profile_serializer(User_obj)  # Convert to Python Data type serializer
        
        return Response(Emp_serializer.data, status=status.HTTP_200_OK)
    except Employee.DoesNotExist:
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return Response({"detail": "Unknown error occurred", "code": "unknown_error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Edit_profile_details(request):
    print("  ",request.data)
    mail_user_info=User.objects.get(email=request.data['mail'])
    print("=1=1=1=1=1=1=",mail_user_info)
    try:
        user_details=edit_profile_serializer(instance=mail_user_info,data=request.data,partial=True)
        print("=========>>>>>>>>>>",user_details)
        if user_details.is_valid():
            print("Data is valid")
            user_details.save()
            return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
        else:
            print("Validation errors:", user_details.errors)
            return Response(user_details.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("MAil user information == >",e)
        
    return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)

def view_all_product(request):
    all_product=product.objects.all()
    return render(request,'all_product.html',{'Product':all_product})


def Product_description(request,slug):
    products=product.objects.get(slug=slug)
    return render(request,'product_description.html',{'Product':products})
    print("******************>",products)

def add_product(request):
    product_info=product.objects.all()
    print("User ========================>>>>",product_info)
    if request.method == "POST":
        try:
            product_name = request.POST.get('Product_name')
            product_price = request.POST.get('Product_price')
            product_description = request.POST.get('Product_description')
            Product_category = request.POST.get('Product_category')
            Product_brand = request.POST.get('Product_brand') 
            Product_size = request.POST.get('Product_size')
            product_image = request.FILES.get('Seller_product_picture')
            data = {
                    'name' : product_name,
                    'price' : int(product_price),
                    'description' : product_description,
                    'category' : Product_category,
                    'brand' : Product_brand,
                    'size' : Product_size
                }
            files = {
                'image': product_image
            }
            print("======================>",data)
            BASEURL = "http://localhost:8000/"
            ENDPOINT ='add_product_api/'
            token=request.COOKIES.get('jwt')
            print("TOKEN",token)
            # Headers for the request
            headers = {
                'Content_Type':'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',
                'Authorization': f'Bearer {token}'
            }
            try:
                resp = requests.post(BASEURL + ENDPOINT, data=data,files=files,headers=headers)
                if resp.status_code == 201:
                    return render(request,'')
            except Exception as e:
                print("Error during API call",resp)
            print("Response status code:", resp.status_code)
            
        except Exception as e:
            print("Data fatching issue",e)
    print(request.user)
    return render(request,'add_product_admin.html',{'product_info':product_info})




from rest_framework import generics

class ProductCreateAPIView(generics.ListCreateAPIView):
    print("API called")
    queryset=product.objects.all()
    serializer_class = product_serializers


################################################
def add_update_product_details(request):
    product_info=product.objects.all()
    print("User ========================>>>>",product_info)
    if request.method == "POST":
        try:
            product_name = request.POST.get('Product_name')
            product_price = request.POST.get('Product_price')
            product_description = request.POST.get('Product_description')
            Product_category = request.POST.get('Product_category')
            Product_brand = request.POST.get('Product_brand') 
            Product_size = request.POST.get('Product_size')
            product_image = request.FILES.get('Seller_product_picture')
            data = {
                    'name' : product_name,
                    'price' : int(product_price),
                    'description' : product_description,
                    'category' : Product_category,
                    'brand' : Product_brand,
                    'size' : Product_size
                }
            files = {
                'image': product_image
            }
            print("======================>",data)
            BASEURL = "http://localhost:8000/"
            ENDPOINT ='update_delete_product/'
            token=request.COOKIES.get('jwt')
            print("TOKEN",token)
            # Headers for the request
            headers = {
                'Content_Type':'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',
                'Authorization': f'Bearer {token}'
            }
            try:
                resp = requests.post(BASEURL + ENDPOINT, data=data,files=files,headers=headers)
            except Exception as e:
                print("Error during API call",resp)
            print("Response status code:", resp.status_code)
            
        except Exception as e:
            print("Data fatching issue",e)
    print(request.user)
    return render(request,'add_product_admin.html',{'product_info':product_info})



        
class ProductUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset=product.objects.all()
    serializer_class = product_serializers

def about(request):
    return render(request,'about.html')


def contact_us(request):
    return render(request,'contact.html')
