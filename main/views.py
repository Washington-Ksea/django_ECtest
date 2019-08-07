from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from main import models
from script.pagenation import get_pagenation, get_page_range
import random

class ProductListView(ListView):
    template_name = 'main/product_list.html'

    def get_queryset(self, **kwargs):
        self.tag = None
        self.sub_tag = None

        self.page_range = None
        
        tag = self.kwargs["tag"]
        sub_tag = self.request.GET.get('sub-tag')
        if tag != 'all':
            if tag.isdecimal():
                #not all or tag dose not exist in the database
                tag = int(tag)
                self.tag = get_object_or_404(
                    models.ProductTag, id=tag
                )

        if self.tag:
            products = models.Product.objects.filter(
                tag=self.tag
            )
        else:
            products = models.Product.objects.filter(active=True)

        if sub_tag:
            if sub_tag.isdecimal():
                self.sub_tag = get_object_or_404(
                    models.ProductSubTag, id=sub_tag
                )
        
        if self.sub_tag:
            products = products.filter(
                sub_tags=self.sub_tag
            )

        
        product_count = products.count()

        #pagenation                
        self.target_page = self.request.GET.get('page')

        display_obj_index, dispaly_obj_num = get_pagenation(product_count, self.target_page)        

        products = products[display_obj_index - dispaly_obj_num: display_obj_index]  

        print(display_obj_index, dispaly_obj_num)
        self.page_range = get_page_range(product_count, self.target_page) 
        
        return products
    
    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['tags'] = models.ProductTag.objects.all()
        context['sub_tags'] = models.ProductSubTag.objects.all()
        context['page_obj'] = self.page_range
        

        return context


    

class ProductDetailView(TemplateView):
    template_name = 'main/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs) 
        #product context
        url = self.kwargs['uuid_url']
        context['product'] = get_object_or_404(
            models.Product, uuid_url=url
        ) 
        
        #product seller context
        USER_DISPLAY_TARGET_NUM = 1
        seller = {}
        seller['seller'] = context['product'].user
        seller['image'] = seller['seller'].get_info(models.UserImage)[0].thumbnail.url
        seller['url'] = seller['seller'].get_info(models.UrlUser)
        
        topic_count = seller['seller'].get_count(models.interast_Topic_User)
        fav_user_count =  seller['seller'].get_count(models.FavoriteUser)
        fav_product_count = seller['seller'].get_count(models.FavoriteProduct)

        if topic_count > USER_DISPLAY_TARGET_NUM:
            seller['topic'] = seller['seller'].get_random_info(models.interast_Topic_User, USER_DISPLAY_TARGET_NUM)
        else:
            seller['topic'] = seller['seller'].get_info(models.interast_Topic_User)

        if fav_user_count > USER_DISPLAY_TARGET_NUM:
            seller['fav_user'] = seller['seller'].get_random_info(models.interast_Topic_User, USER_DISPLAY_TARGET_NUM)
        else:
            seller['topic'] = seller['seller'].get_info(models.interast_Topic_User) 

        if topic_count > USER_DISPLAY_TARGET_NUM:
            seller['topic'] = seller['seller'].get_random_info(models.interast_Topic_User, USER_DISPLAY_TARGET_NUM)
        else:
            seller['topic'] = seller['seller'].get_info(models.interast_Topic_User)
        
        context['seller'] = seller

        #login user context
        context['seller_is_favorite'] = None
        context['product_is_favorite'] = None
        if self.request.user.is_authenticated:
            user_name = self.request.user.username
            if user_name is not 'Anonymous':
                login_user = get_object_or_404(
                    models.User, username=user_name
                )  
                for favorite_user in login_user.get_info(models.FavoriteUser):
                    if favorite_user.target.id == context['product'].user.id:
                        context['seller_is_favorite'] = True
                        print('seller is favorite')

                for favorite_product in login_user.get_info(models.FavoriteProduct):
                    if favorite_product.product.id == context['product'].id:
                        context['product_is_favorite'] = True  
                        print('product is favorite')
        
        return context


