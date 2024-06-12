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
                        attrs['employee'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")
        # if not check_password(password, User.Password):
        #     raise serializers.ValidationError("Invalid email or password.")
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


class edit_profile_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_number","email","dob","Gender","first_name","last_name"]
        print("CALLAED1")
        
    def update(self,instance,validated_data):
        print("CALLAED2")
        try:
            print("//////////////////////UPDATE DATA",validated_data)
            print("***********",instance)
            instance.phone_number = validated_data.get('phone_number', instance.phone_number)
            instance.email = validated_data.get('email', instance.email)
            instance.dob = validated_data.get('dob', instance.dob)
            instance.Gender = validated_data.get('Gender', instance.Gender)
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.save()
            return instance
        except Exception as e:
            print("Maybe some error instance ",e)
    
        
        # def update(self, instance, validated_data):
        # user_data = validated_data.pop('user')
        # user = instance.user

        # instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        # instance.dob = validated_data.get('dob', instance.dob)
        # instance.gender = validated_data.get('gender', instance.gender)
        # instance.bio = validated_data.get('bio', instance.bio)
        # instance.location = validated_data.get('location', instance.location)
        # instance.save()

        # user.first_name = user_data.get('first_name', user.first_name)
        # user.last_name = user_data.get('last_name', user.last_name)
        # user.email = user_data.get('email', user.email)
        # user.save()




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