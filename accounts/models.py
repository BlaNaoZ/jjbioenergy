from django.db import models
from django.contrib.auth.models import (
    AbstractUser, BaseUserManager, AbstractBaseUser, UserManager
)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    
    """
    Fields required for a user instance.
    Email and password - used for authentication.
    Flags - used for permission across the app.
    User type - to choose and create an instance of a certain user type (Supplier, Heat Buyer or Foundation Industry).
    """

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    supplier_flag = models.BooleanField(default=False) # a admin user; non super-user
    heat_buyer_flag = models.BooleanField(default=False)
    foundation_industry_flag = models.BooleanField(default=False) # a admin user; non super-user

    ADMIN_CHOICE = 'Admin'
    SUPPLIER_CHOICE = 'Supplier'
    HEAT_BUYER_CHOICE = 'Heat Buyer'
    FOUNDATION_INDUSTRY_CHOICE = 'Foundation Industry'
    
    """
    The choices format is as follows:
    ((Data to be saved in the database), (Message to be shown for the user))
    """

    USER_CHOICES = (
        (ADMIN_CHOICE, 'Admin'),
        (SUPPLIER_CHOICE, 'Supplier'),
        (HEAT_BUYER_CHOICE, 'Heat Buyer'),
        (FOUNDATION_INDUSTRY_CHOICE, 'Foundation Industry'),
    )

    user_type = models.CharField(max_length=25, choices=USER_CHOICES, default=HEAT_BUYER_CHOICE)
    
    favourites = models.ManyToManyField("app.Reference", related_name='favorited_by')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.


    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    objects = UserManager()


class FoundationIndustry(models.Model):
    """
    FoundationIndustry is a subclass of the User class.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200)

    METAL_CHOICE = 'Metal'
    CERAMICS_CHOICE = 'Ceramics'
    CHEMICALS_CHOICE = 'Chemicals'
    PAPER_CHOICE = 'Paper'
    CEMENT_CHOICE = 'Cement'
    GLASS_CHOICE = 'Glass'

    LEVEL_ONE_CHOICES = (
        (METAL_CHOICE, 'Metal'),
        (CERAMICS_CHOICE, 'Ceramics'),
        (CHEMICALS_CHOICE, 'Chemicals'),
        (PAPER_CHOICE, 'Paper'),
        (CEMENT_CHOICE, 'Cement'),
        (GLASS_CHOICE, 'Glass'),
    )

    STAINLESS_STEEL_CHOICE = 'Stainless steel'
    ALLUMINIUM_CHOICE = 'Alluminium'

    LEVEL_TWO_CHOICES = (
        (STAINLESS_STEEL_CHOICE, 'Stainless steel'),
        (ALLUMINIUM_CHOICE, 'Alluminium'),
    )

    level_one = models.CharField(max_length=20, choices=LEVEL_ONE_CHOICES, default=METAL_CHOICE)
    level_two = models.CharField(max_length=20, choices=LEVEL_TWO_CHOICES, default=STAINLESS_STEEL_CHOICE)

    """
    Used to show the plural of FoundationIndustry users as follows (original was Foundation Industrys)
    """
    class Meta:
        verbose_name_plural = "Foundation Industries"
    
    def __str__(self):
        return self.name


class HeatBuyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)

    DHN_CHOICE = 'DHN'
    INDUSTRY_CHOICE = 'Industry'
    COMMERCIAL_CHOICE = 'Commercial'
    UNI_CHOICE = 'Uni'

    LEVEL_ONE_CHOICES = (
        (DHN_CHOICE, 'DHN'),
        (INDUSTRY_CHOICE, 'Industry'),
        (COMMERCIAL_CHOICE, 'Commercial'),
        (UNI_CHOICE, 'Uni'),
    )

    HOTEL_CHOICE = 'Hotel'
    SUPERMARKET_CHOICE = 'Supermarket'

    LEVEL_TWO_CHOICES = (
        (HOTEL_CHOICE, 'Hotel'),
        (SUPERMARKET_CHOICE, 'Supermarket'),
    )

    level_one = models.CharField(max_length=20, choices=LEVEL_ONE_CHOICES, default=DHN_CHOICE)
    level_two = models.CharField(max_length=20, choices=LEVEL_TWO_CHOICES, default=HOTEL_CHOICE)

    class Meta:
        verbose_name_plural = "Heat Buyers"

    def __str__(self):
        return self.name

class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200)
    
    POWER_GEN_CHOICE = 'Power Gen'
    HEAT_EXCHANGE_CHOICE = 'Heat Exchange'
    TGS_CHOICE = 'TGS'
    HEAT_PUMPS_CHOICE = 'Heat Pumps'

    LEVEL_ONE_CHOICES = (
        (POWER_GEN_CHOICE, 'Power Gen'),
        (HEAT_EXCHANGE_CHOICE, 'Heat Exchange'),
        (TGS_CHOICE, 'TGS'),
        (HEAT_PUMPS_CHOICE, 'Heat Pumps'),
    )

    STEAM_POWER_CHOICE = 'Steam Power Gen'
    ORC_CHOICE = 'ORC'

    LEVEL_TWO_CHOICES = (
        (STEAM_POWER_CHOICE, 'Steam Power Gen'),
        (ORC_CHOICE, 'ORC'),
    )

    level_one = models.CharField(max_length=20, choices=LEVEL_ONE_CHOICES, default=POWER_GEN_CHOICE)
    level_two = models.CharField(max_length=20, choices=LEVEL_TWO_CHOICES, default=STEAM_POWER_CHOICE)

    website = models.URLField(max_length=100, default="None")

    def __str__(self):
        return self.name
