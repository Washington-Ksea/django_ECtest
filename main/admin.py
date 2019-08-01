from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from . import models

 
  
@admin.register(models.User) 
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (
            'Personal info',
            {'fields': ('habitat', 'introduction')},
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'user_permissions',
                )
            },
        ),
        (
            'Important dates',
            {'fields': ('last_login', 'date_joined')},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            },
        ),
    )
    list_display = (
        'username',
        'email',
        'is_staff',
    )
    search_fields = ('username','email')
    ordering = ('email',)

@admin.register(models.UrlUser)
class UrlUserAdmin(admin.ModelAdmin):
    list_display= ('name', 'url')
    search_fields = ('user__username',)


@admin.register(models.interast_Topic_User)
class interast_Topic_UserAdmin(admin.ModelAdmin):
    list_display= ('topic_tag',)
    search_fields = ('user__username',)

@admin.register(models.UserImage)
class UserImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_tag', 'user_name', 'thumbnail') 
    readonly_fields = ('thumbnail',)
    search_fields = ('user__username',) 
    
    def thumbnail_tag(self, obj): 
        if obj.thumbnail: 
            return format_html( 
                '<img src="%s"/>' % obj.thumbnail.url 
            ) 
        return "-"
    
    thumbnail_tag.short_description = "Thumbnail"
    def user_name(self, obj): 
        return obj.user.username 

@admin.register(models.FavoriteUser)
class FavoriteUserAdmin(admin.ModelAdmin):
    list_display= ('target', )
    search_fields = ('user__username',)

@admin.register(models.SecretProfile)
class SecretProfileAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 
                    'account_holder', 
                    'account_number',
                    'Deposit_type',
                    'financial_institution_code',
                    'branch_code')
    search_fields = ('user__email', )
    

@admin.register(models.ProductTag)
class ProductTagAdmin(admin.ModelAdmin): 
    list_filter = ('active',) 
    search_fields = ('name',) 

   

@admin.register(models.ProductSubTag)
class ProductTagAdmin(admin.ModelAdmin): 
    list_filter = ('active',) 
    search_fields = ('name',) 
    


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'price', 'uuid_url')}),
        (
            'Info',
            {'fields': ('description',)},
        ),
        (
            'Permissions',
            {
                'fields': (
                    'active',
                    'in_stock',
                )
            },
        ),
    )
    list_display = ('name', 'price', 'tag')
    list_filter = ('active', 'in_stock', 'date_updated')
    #list_editable = ('in_stock',)
    search_fields = ('user__username', )
    autocomplete_fields = ('sub_tags',) 


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_tag', 'product_name') 
    readonly_fields = ('thumbnail',)
    search_fields = ('product__name',) 

    def thumbnail_tag(self, obj): 
        if obj.thumbnail: 
            return format_html( 
                '<img src="%s"/>' % obj.thumbnail.url 
            ) 
        return "-"
    
    thumbnail_tag.short_description = "Thumbnail"
    def product_name(self, obj): 
        return obj.product.name 

@admin.register(models.FavoriteProduct)
class FavoriteProductImageAdmin(admin.ModelAdmin):
    list_display= ('product', )
    search_fields = ('user__name',)

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'product')}),
        (
            'Info',
            {'fields': ('status',)},
        ),
        (
            'Evaluation',
            {
                'fields': (
                    'star',
                    'comment',
                )
            },
        ),
    )
    list_display=('id', 'status', 'star',)
    search_fields = ('user__name', 'product__name')

