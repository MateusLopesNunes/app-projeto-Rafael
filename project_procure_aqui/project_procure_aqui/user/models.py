from email.policy import default
from django.db import models
from product.models import City, Product
from django.contrib.auth import models as auth_models
from django.utils import timezone
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  

#from django.utils.translation import ugettext_lazy

class UserManager(auth_models.BaseUserManager):
    def _create_user(self, username, email, password, is_superuser, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                 is_staff=True, is_active=True,
                 is_superuser=is_superuser, last_login=now,
                 date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user=self._create_user(username, email, password, True,
                 **extra_fields)
        user.is_active=True
        user.save(using=self._db)
        return user
    
class User(auth_models.AbstractUser, auth_models.PermissionsMixin):
    sexEnum = (
        ("Masculino", "masculine"),
        ("Feminino", "feminine"),
        ("Outro", "other"),
    )

    username = models.CharField(max_length=100)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    sex = models.CharField(choices=sexEnum, max_length=20, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)

    object = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    def __str__(self):
        return self.username


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )

class ListOfProducts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

