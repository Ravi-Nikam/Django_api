from rest_framework import serializers
from .models import Employee,User
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate

class EmpSerializers(serializers.ModelSerializer):
    # country = serializers.SerializerMethodField()
    class Meta:
        model = User
        # fields = ['phone_number','email','Gender','first_name','password','last_name','dob']  # All field
        fields = "__all__"
        # extra_kwargs = {
        #     'password': {'write_only': True},
        #     'first_name': {'required': True},
        #     'last_name': {'required': True},
        #     'Gender': {'required': True},
        #     'phone_number': {'required': True},
        #     'dob': {'required': True}
        # }
    print("6***************************")
    def validate(self,data):
        for fields in User.REQUIRED_FIELDS:
            if fields not in data:
                raise serializers.ValidationError("Fields Require",fields)
        print("big data",data)
        return data
    
    def create(self, validated_data):
        validated_data['password']=make_password(validated_data['password'])   # Adjust if Employee model does not have set_password method
        user = User.objects.create(**validated_data)
        # Assuming you want to set a hashed password or do any other processing
        return user
    


class LoginSerializers(serializers.Serializer):
    Email = serializers.CharField(required=True)
    Password = serializers.CharField()
    def validate(self,attrs):
        # Email Attribute comes from Email = serializers.CharField(required=True) this and same for Password
        # They Are same as the Model attributes 
        # this also display in the api attributes 
        # try to make it in lowercase
        # email=attrs.get('Email') 
        # password = attrs.get('Password')
        usr=authenticate(email=attrs['Email'],password=attrs['Password'])
        
        if not attrs['Email'] or not attrs['Password']:
            print("?????????????>>>>>>>>>>>>>>>>",usr)
            raise serializers.ValidationError("Both email and password are required.")
        try:
            if usr:
                print("YES USER")
                if User.objects.filter(email=attrs['Email']).exists():
                    print("Till this done")
                    user = User.objects.get(email=attrs['Email'])
                    print("-------->",user)
                    if check_password(attrs['Password'],user.password):
                        print("TILL GOOD")
                        print("Here is an Emplpoyee",user)
                        print("DATA NOT FOUND")
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")
        # if not check_password(password, User.Password):
        #     raise serializers.ValidationError("Invalid email or password.")
        attrs['employee'] = user

        return attrs
    

class profile_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_number",
                "email",
                "dob",
                "Gender",
                "first_name",
                "last_name"]


# class LoginSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Employee
#         fields = ['Email', 'Password']
    
#     def validate(self,data):
#         email = data.get('Email')
#         password = data.get('Password')
#         print(email,password)
#         try:
#             employee = Employee.objects.get(Email=email)
#         except Employee.DoesNotExist:
#             raise serializers.ValidationError("Invalid email or password.")
        
#         if not check_password(password, employee.Password):
#             raise serializers.ValidationError("Invalid email or password.")
#         print("=============>",data)
#         return data