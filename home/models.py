from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User


class CustomUserManager(BaseUserManager):
    """
    Custom user manager.
    """

    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.
    """

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class ContactUs(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    email = models.CharField(max_length=100, verbose_name="Email")
    desc = models.TextField(verbose_name="Description")
    date = models.DateField(verbose_name="Date")

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100, verbose_name="Product Name")
    category = models.CharField(max_length=50, default="", verbose_name="Category")
    subcategory = models.CharField(max_length=50, default="", verbose_name="Subcategory")
    price = models.IntegerField(default=0, verbose_name="Price")
    desc = models.TextField(verbose_name="Description")
    pub_date = models.DateField(verbose_name="Publication Date")
    image = models.ImageField(upload_to="cafeItems/images", default="", verbose_name="Image")

    def __str__(self):
        return self.product_name


class CartItem(models.Model):
    # Use the custom user model from AUTH_USER_MODEL
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"

    
class Reviews(models.Model):
    review_id = models.AutoField(primary_key=True)
    reviewer_name = models.CharField(max_length=50, default="", verbose_name="Reviewer Name")
    review = models.TextField(default="", verbose_name="Review")
    review_date = models.DateField(verbose_name="Review Date")

    def __str__(self):
        return self.reviewer_name


class Checkout(models.Model):
    """
    Model representing a checkout process.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="checkouts")
    name = models.CharField(max_length=255, verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    address = models.CharField(max_length=255, verbose_name="Address")
    city = models.CharField(max_length=255, verbose_name="City")
    state = models.CharField(max_length=255, verbose_name="State")
    zipcode = models.CharField(max_length=10, verbose_name="Zipcode")
    country = models.CharField(max_length=255, verbose_name="Country")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return f"{self.name}'s Checkout"


class Order(models.Model):
    """
    Model representing an order.
    """
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE, related_name="orders")
    product_name = models.CharField(max_length=255, verbose_name="Product Name")
    quantity = models.IntegerField(verbose_name="Quantity")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return f"{self.product_name} (x{self.quantity})"

class Payment(models.Model):
    """
    Model representing a payment.
    """
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE, related_name="payments")
    payment_method = models.CharField(max_length=255, verbose_name="Payment Method")
    payment_date = models.DateTimeField(verbose_name="Payment Date")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount")

    def __str__(self):
        return f"{self.checkout.name}'s Payment"