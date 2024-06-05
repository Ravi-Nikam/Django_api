from rest_framework import serializers
from .models import Employee
from django.contrib.auth.hashers import make_password,check_password


class EmpSerializers(serializers.ModelSerializer):
    # country = serializers.SerializerMethodField()
    class Meta:
        print("=========================> called serialzier")
        model = Employee
        # fields = ['Emp_id','Emp_Name'] # On Specific field
        fields = '__all__'  # All field
        # exclude = ['Emp_id',] # except Emp_id
    def validate(self,data):
         # Add any custom validation logic if needed
        return data
    
    def create(self, validated_data):
        validated_data['Password']=make_password(validated_data['Password'])   # Adjust if Employee model does not have set_password method
        employee = Employee.objects.create(**validated_data)
        # Assuming you want to set a hashed password or do any other processing
        return employee
    


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
        print("--------->>aaattrs",attrs)
        return attrs

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