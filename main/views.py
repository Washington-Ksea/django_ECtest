from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView

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
    

