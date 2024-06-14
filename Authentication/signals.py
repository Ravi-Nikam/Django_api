from allauth.account.signals import user_signed_up
from django.dispatch import receiver

@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    user.email = user.socialaccount_set.filter(provider='google')[0].extra_data['email']
    print("user.email",user.email)
    user.save()
