from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import User


class AccountDatas(models.Model):
    choices = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    roles = [
        ('Owner', 'Owner'),
        ('Operator', 'Operator'),
        ('Rob', 'Rob'),
    ]

    owner: User = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Owner', related_name='account_datas')
    role = models.CharField(max_length=8, choices=roles, default='Operator', verbose_name='Role')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg', blank=True, null=True, verbose_name='Avatar')
    gender = models.CharField(max_length=6, choices=choices, default='Male', verbose_name='Gender')
    phone = models.CharField(max_length=13, verbose_name='Phone number', validators=[MinLengthValidator(13)])
    datas = models.TextField(auto_created=True, default='{}', verbose_name='Extra datas')
    last_online = models.CharField(max_length=200, blank=True, null=True, verbose_name='Last online')

    def get_email(self):
        return self.owner.email or 'cleanpharm.uz'

    def __str__(self):
        return str(self.owner.first_name or self.owner.username)

    class Meta:
        verbose_name = 'Account data'
        verbose_name_plural = 'Account datas'

class Leads(models.Model):
    name = models.CharField(max_length=200, verbose_name='Customer name')
    phone = models.CharField(max_length=13, verbose_name='Phone number', validators=[MinLengthValidator(13)])
    request_date = models.CharField(max_length=10, verbose_name='Request date', validators=[MinLengthValidator(10)])
    addresses = [
        ("Tashkent", "Tashkent"),
        ("Andijan", "Andijan"),
        ("Bukhara", "Bukhara"),
        ("Jizzakh", "Jizzakh"),
        ("Kashkadarya", "Kashkadarya"),
        ("Navoi", "Navoi"),
        ("Namangan", "Namangan"),
        ("Samarkand", "Samarkand"),
        ("Surkhandarya", "Surkhandarya"),
        ("Syrdarya", "Syrdarya"),
        ("Tashkent region", "Tashkent region"),
        ("Fergana", "Fergana"),
        ("Khorezm", "Khorezm"),
        ("Republic of Karakalpakstan", "Republic of Karakalpakstan")
    ]
    address = models.CharField(max_length=30, choices=addresses, verbose_name='Address')
    products = [
        ("Lactos", "Lactos"),
        ("Laditex", "Laditex"),
        ("PerfectMan", "PerfectMan"),
        ("Tribgen", "Tribgen")
    ]

    product = models.CharField(max_length=50, choices=products, verbose_name='Product')

    statuses = [
        ("New", "New"),
        ("Refused", "Refused"),
        ("Approved", "Approved"),
        ("Need approved", "Need approved")
    ]

    status = models.CharField(max_length=50, choices=statuses, verbose_name='Lead status', default='New', auto_created=True)
    operator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Operator', blank=True, null=True, auto_created=True)
    quantity = models.IntegerField(verbose_name='Sold quantity', default=0, auto_created=True)
    price = models.BigIntegerField(verbose_name='Price sold', blank=True, null=True, auto_created=True)
    sold_date = models.CharField(max_length=10, verbose_name='Sold date', blank=True, null=True, validators=[MinLengthValidator(10)])
    comments = models.TextField(verbose_name='Comments', editable=False, auto_created=True, default='[]')
    regwarded = models.BooleanField(verbose_name='Regwarded', default=False)
    call_count = models.IntegerField(verbose_name='Call count', default=0)
    lead_calldate = models.CharField(max_length=10, verbose_name='Call date', blank=True, null=True, validators=[MinLengthValidator(10)])

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'


class Lead_comments(models.Model):
    owner = models.ForeignKey(AccountDatas, on_delete=models.CASCADE, verbose_name='Comment owner')
    text = models.TextField(verbose_name='Content')
    pinned_file = models.FileField(upload_to='comments/', verbose_name='Pinned file', blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name='Upload date')
    lead = models.ForeignKey(Leads, on_delete=models.CASCADE, verbose_name='Refer to lead')

    def __str__(self):
        return str(self.owner.owner.username)

    class Meta:
        verbose_name = 'Lead comment'
        verbose_name_plural = 'Leads comments'