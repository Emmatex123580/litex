from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.
from .managers import CustomUserManager
import uuid
from phone_field import PhoneField
class CustomUser(AbstractUser):
    username = None
    uid = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False )
    email = models.EmailField(_("email address"), blank=False, unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False )
    date_of_birth = models.DateField(_('date of birth'), max_length=150, blank=False)
    phone_number = PhoneField(_('phone'), max_length=31, blank=False)
    verified = models.BooleanField(_('verified'), default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','date_of_birth','phone_number']
    objects = CustomUserManager()
    def __str__(self):
        return self.email


    
class Asset(models.Model):
    name = models.CharField(max_length=30)
    status = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}, {self.status}'

class Crypto(models.Model):
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.name}, {self.status}'

class WalletAddress(models.Model):
    address = models.TextField()

    def __str__(self):
        return f'wallet is, {self.address}'

# class Debit(models.Model):
#     transactionReference = models.CharField() 
#     amount = models.DecimalField()
#     phone_number = models.CharField()


class Wallets(models.Model):
    uid = models.UUIDField(primary_key =True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True)
    balance = models.DecimalField(_('balance'), max_digits=100, decimal_places=2)
    account_name = models.CharField(_("account name"), max_length=200)
    account_number = models.CharField(_('account number'), max_length=100)
    bank = models.CharField(_('bank'), max_length=100)
    phone_number = models.CharField(_('phone_number'), max_length=100)
    password = models.CharField(_('password'), max_length=200)
    created = models.DateTimeField(auto_now_add=True)

class WalletTransaction(models.Model):
    class STATUS(models.TextChoices):
        PENDING = 'pending', _('pending')
        SUCCESS = 'success', _('success')
        FAIL = 'fail', _('fail')

    class TransactionType(models.TextChoices):
        BANK_TRANSFER_FUNNDING = 'funding', _('Bank transfer funding')
        BANK_TRANSFER_PAYOUT = 'payout', _('Bank transfer payout')
        DEBIT_USER_WALLET = 'debit user wallet', _('Debit user wallet')
        CREDIT_USER_WALLET = 'credit user wallet ', _('credit user wallet')

    transaction_id = models.CharField(_('transaction id'), max_length=250)
    status = models.CharField(max_length=200, null=True,
            choices = STATUS.choices,
            default = STATUS.PENDING )
    transaction_type = models.CharField(max_length=250, null=True,
            choices = TransactionType.choices,
            )
    wallet = models.ForeignKey(Wallets, on_delete=models.SET_NULL, null=True)
    amount = models .DecimalField(_('amount'), max_digits=100, decimal_places=2)
    date = models.CharField(_('date'), max_length=200)