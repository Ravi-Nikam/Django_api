from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password,check_password


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, gender,phone_number, dob, password=None):
        user = self.model(email=email,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            phone_number=phone_number,
            dob=dob)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email, first_name, last_name, gender, phone_number, dob, password=None):
        user = self.create_user(email=email,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            phone_number=phone_number,
            dob=dob,
            password=password)
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

        
        
        