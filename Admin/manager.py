from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password,check_password

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, Gender, phone_number, dob, password=None):
        # if not email:
        #     raise ValueError('The Email field is required')
        # if not first_name:
        #     raise ValueError('The First Name field is required')
        # if not last_name:
        #     raise ValueError('The Last Name field is required')
        # if not phone_number:
        #     raise ValueError('The Phone Number field is required')
        # if not dob:
        #     raise ValueError('The Date of Birth field is required')
        print("2***************************")
        email = self.normalize_email(email)
        hashed_password = make_password(password)
        print("*******************************444",hashed_password)
        # user = self.model(email=email,**extra_fields)
        user = self.model(
            email=email,
            first_name=first_name,
            password = hashed_password,
            last_name=last_name,
            Gender=Gender,
            phone_number=phone_number,
            dob=dob,
        )
        # user.set_password(password)
        user.save(using = self._db)
        
        return user
        
        
    def create_superuser(self,email,first_name, last_name, Gender, phone_number, dob, password=None,**extra_fields):
        print("code for super")
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            Gender=Gender,
            phone_number=phone_number,
            dob=dob,
        )
        # extra_fields.setdefault('is_staff', True)  # Set is_staff to True
        # extra_fields.setdefault('is_superuser', True)  # Set is_superuser to True
        user.is_staff = True
        user.is_admin=True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        
        return user
        # extra_fields.setdefault('is_staff',True)
        # extra_fields.setdefault('is_superuser',True)
        # extra_fields.setdefault('is_active',True)
        # extra_fields['first_name'] = ''
        # extra_fields['last_name'] = ''
        # extra_fields['Gender'] = ''
        # extra_fields['dob'] = ''
        # extra_fields['phone_number'] = ""
        
        
        try:
            return self.create_user(email,password, **extra_fields)
        except Exception as e:
            print("Error in creating superuser",e)
        
        
        