from rest_framework import serializers
from .models import Employee,CustomUser
from django.contrib.auth.hashers import make_password,check_password
    
class EmpSerializers(serializers.ModelSerializer):
    # country = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['phone_number','email','Gender','first_name','password','last_name']  # All field
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self,data):
        print("big data",data)
        return data
    
    def create(self, validated_data):
        print("validate data",validated_data)
        validated_data['password']=make_password(validated_data['password'])   # Adjust if Employee model does not have set_password method
        user = CustomUser.objects.create(**validated_data)
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
        email=attrs.get('Email') 
        password = attrs.get('Password')
        print("PASSWORD CHECKER IS CHECKED",password)
        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")
        try:
            employee = Employee.objects.get(Email=email)
            print("Here is an Emplpoyee",employee)
            print("DATA NOT FOUND")
        except Employee.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")
        if not check_password(password, employee.Password):
            raise serializers.ValidationError("Invalid email or password.")
        
        attrs['employee'] = employee

        return attrs
    
    


class profile_serializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["First_Name","Last_Name","Email","Phone_Number","Gender"]


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