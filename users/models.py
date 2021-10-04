import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string


class User(AbstractUser):
    """Custom User model"""

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )
    LANGUAGE_ENGLISH = "en"
    LANGUAGE_HINDI = "hin"
    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_HINDI, "Hindi"),
    )
    CURRENCY_USD = "usd"
    CURRENCY_INR = "inr"
    CURRENCY_CHOICES = (
        (CURRENCY_USD, "USD"),
        (CURRENCY_INR, "INR"),
    )
    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
    )
    avatar = models.ImageField(blank=True, upload_to="avatars")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    bio = models.TextField(default="")
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, blank=True)
    currency = models.CharField(choices=CURRENCY_CHOICES, blank=True, max_length=3)
    superhost = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=20, default="", blank=True)
    login_method = models.CharField(
        max_length=20, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string(
                "emails/verify_email.html",
                context={"secret": secret, "name": self.username},
            )
            send_mail(
                "Verify Airbnb Account",
                strip_tags(html_message),
                settings.EMAIL_HOST_USER,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        return
