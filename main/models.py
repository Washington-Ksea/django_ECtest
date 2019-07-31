from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, RegexValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail

import uuid
from script.get_random import get_random_int_by_string


class User(AbstractUser):
    """Custom user to perform authentication by email """
    username_validator = UnicodeUsernameValidator()
    username_regex = RegexValidator(regex=r'^[a-zA-Z0-9][a-zA-Z0-9\-]+', message="ユーザネームに使用できない文字が指定されています。")
    username = models.CharField(_('username'), max_length=150, unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator, username_regex, MinLengthValidator(5)],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField('emial address', unique=True)

    #nick_name = models.CharField(_('ユーザーネーム'), max_length=50, default=get_random_int_by_string)
    habitat = models.CharField(_('だいたいの生活地域'), max_length=100, blank=True, null=True)
    introduction = models.TextField(_('自己紹介'), max_length=500, blank=True, null=True)
    
    def get_info(self, get_model):
        return get_model.objects.select_related('user').filter(user__id=self.id)


class UrlUser(models.Model):
    """url defined by user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    user_url = models.URLField(max_length=200)
    
    def __str__(self):
        return self.name


class interast_Topic_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    topic_tag = models.CharField(max_length=50)

    def __str__(self):
        return self.topic_tag


class SecretProfile(models.Model):
    """Information required for bank transfer separately"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone_regex = RegexValidator(regex=r'^\d{9,12}$', message="電話番号の桁が足りません")
    account_number_regex = RegexValidator(regex=r'^\d{7,7}$', message="口座番号を入力してください")
    financial_institution_code_regex = RegexValidator(regex=r'^\d{4,4}$', message="口座番号を入力してください")
    branch_code_regex = RegexValidator(regex=r'^\d{3,3}$', message="口座番号を入力してください")

    deposit_type_state = ((10, '普通預金'), (20, '当座預金'))
    
    phone_number = models.CharField(validators=[phone_regex], max_length=12, default='')
    account_holder = models.CharField(_("口座名義"), max_length=50, default='')
    account_number = models.CharField(_('口座番号'), max_length=7, validators=[account_number_regex], default='')
    Deposit_type = models.IntegerField(choices=deposit_type_state, default=10)
    financial_institution_code = models.CharField(_('金融機関コード'), max_length=4, 
                                                validators=[financial_institution_code_regex], default='')
    branch_code = models.CharField(_('金融機関コード'), max_length=3, validators=[branch_code_regex], default='')

    class Meta:
        unique_together = (
            ('account_number', 'financial_institution_code')
        )
    def __str__(self):
        return self.account_holder

class UserImage(models.Model):
    """Image displayed on user screen"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user-images')
    thumbnail = models.ImageField(upload_to='user-thumbnails', null=True)
    

class FavoriteUser(models.Model):
    """Favorites model for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target-user+')
    favorite = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite-user+')


class BlockUser(models.Model):
    """Block model for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target-user+')
    block_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='block-user+')

    def __str__(self):
        return self.block_user.username

class ProductTag(models.Model):
    """main tag for product"""
    name = models.CharField(max_length=32, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ProductSubTag(models.Model):
    """sub tag for prodacut"""
    name = models.CharField(max_length=32, unique=True)
    #slug = models.SlugField(max_length=48)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid_url = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    tag = models.ForeignKey(ProductTag, on_delete=models.PROTECT)
    sub_tags = models.ManyToManyField(ProductSubTag, blank=True)

    def get_info(self, get_model):
        return get_model.objects.select_related('product').filter(product__id=self.id)


    def __str__(self):
        return self.name
 
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product-images')
    thumbnail = models.ImageField(upload_to="product-thumbnails", null=True)


class FavoriteProduct(models.Model):
    """Favorite model for product"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite_product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    STATUSES = ((10, 'Negotiation'), (20, 'GotoSettle'), (30, 'Paid'))
    status = models.IntegerField(choices=STATUSES, default=10)

    #order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    star = models.IntegerField(_('star'), blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(_('Comment'), blank=True, null=True, default='')
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)







