from collections import Counter
import csv
import os.path
import sys
import linecache

from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from django.template.defaultfilters import slugify
from django.db import transaction

import uuid

from main import models
#from main import signals

def failure(e):
    exc_type, exc_obj, tb=sys.exc_info()
    lineno=tb.tb_lineno
    print(str(lineno) + ":" + str(type(e)))
    exit(-1)


class Command(BaseCommand):
    help = 'Import user data'

    def add_arguments(self, parser):
        """how to use ./manage.py csvfile image_basedir"""
        parser.add_argument("csvfile", type=open)
        parser.add_argument("user_basedir", type=str)
        parser.add_argument("product_basedir", type=str)
    
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Importing user data")

        csv_reader = csv.DictReader(options.pop("csvfile"))
        
        row_index = []
        row_users = []
        csv_rows = []

        images = [] #for create thumbnail
        for_save_objects = []
        
        try:
            #User information create
            for row in csv_reader:    
                user, created = models.User.objects.get_or_create(
                    username=row['username'], 
                    email=row['email'],
                    habitat=row['habitat'],
                    introduction = row['introduction']
                )
                for_save_objects.append(user)
                urluser, created = models.UrlUser.objects.get_or_create(
                    user=user,
                    name=row['url_name'],
                    url=row['url']
                )
                for_save_objects.append(urluser)
                topic_tags = row['topic'].split("|")
                for tag in topic_tags:
                    topic, created = models.interast_Topic_User.objects.get_or_create(
                        user=user,
                        topic_tag=tag
                    )
                    for_save_objects.append(topic)
                
                secretprof, created = models.SecretProfile.objects.get_or_create(
                    user=user,
                    phone_number=row['phone'],
                    account_holder=row['holder'],
                    account_number=row['anum'],
                    Deposit_type=int(row['depo']),
                    financial_institution_code=row['ficode'],
                    branch_code=row['bcode'],
                )
                for_save_objects.append(secretprof)
                
                #userImage
                with open(
                    os.path.join(
                        options["user_basedir"],
                        row['uimage'],
                    ), 'rb',
                ) as f:
                    userimage, created = models.UserImage.objects.get_or_create(
                        user=user,
                        image=ImageFile(f, name=row['uimage'])
                    )
                    images.append(userimage)
                
                row_index.append(row['id'])
                row_users.append(user)
                csv_rows.append(row)
                
            #User Favorite and Block 
            for ind in range(len(row_index)):
                
                user = row_users[ind]
                row = csv_rows[ind]

                favusers = row['favuser'].split('|')
                for favuser in favusers:
                    if favuser != "":
                        favuser=row_users[int(favuser)-1]
                        favorite_user, created = models.FavoriteUser.objects.get_or_create(
                            user=user,
                            target=favuser
                        )
                        for_save_objects.append(favorite_user)
                
                blockusers = row['blockuser'].split('|')
                for blockuser in blockusers:
                    if blockuser != "":
                        blockuser=row_users[int(blockuser)-1]
                        block_user, created = models.BlockUser.objects.get_or_create(
                            user=user,
                            target=blockuser
                        )
                        for_save_objects.append(block_user)

            
            temp_ptag = []
            product_tags = []
            temp_subtag = []
            subproduct_tags = []
            products = []
            
            #create tags
            for ind in range(len(csv_rows)):
                ptag = csv_rows[ind]['ptag']
                if ptag not in temp_ptag:
                    product_tag, created = models.ProductTag.objects.get_or_create(
                        name=ptag
                    )
                    product_tags.append(product_tag)
                    temp_ptag.append(ptag)
                    for_save_objects.append(product_tag)
                
                subptags = csv_rows[ind]['sptag'].split('|')
                for subtag in subptags:
                    if subtag not in temp_subtag and subtag != '':
                        subproduct_tag, created = models.ProductSubTag.objects.get_or_create(
                            name=subtag
                        )
                        subproduct_tags.append(subproduct_tag)
                        temp_subtag.append(subtag)
                        for_save_objects.append(subproduct_tag)

            #create product
            for ind in range(len(csv_rows)):
                user = row_users[ind]
                row = csv_rows[ind]

                ptag = row['ptag']
                product_tag = product_tags[temp_ptag.index(ptag)]

                product, created = models.Product.objects.get_or_create(
                    user=user,
                    name=row['pname'],
                    description=row['pdisc'],
                    price=int(row['price']),
                    tag = product_tag
                )

                subptags = row['sptag'].split('|')
                for subtag in subptags:
                    if subtag != '':
                        subproduct_tag = subproduct_tags[temp_subtag.index(subtag)]
                        product.sub_tags.add(subproduct_tag) #add is for manyTomany
                
                for_save_objects.append(product)
                
                
                #create product image
                for uimage in row['pimage'].split('|'):
                    with open(
                        os.path.join(
                            options["product_basedir"],
                            uimage,
                        ), 'rb',
                    ) as f:
                        productimage, created = models.ProductImage.objects.get_or_create(
                            product=product,
                            image=ImageFile(f, name=uimage)
                        )
                        images.append(productimage)

                products.append(product)

            #Create favorite product
            for ind in range(len(csv_rows)):
                user = row_users[ind]
                row = csv_rows[ind]
                for temp_favprod in row['fproduct'].split('|'):
                    if temp_favprod != "":
                        favoriteproduct, created = models.FavoriteProduct.objects.get_or_create(
                            user=user,
                            product=products[int(temp_favprod)-1]
                        )
                        for_save_objects.append(favoriteproduct)

            #Create Order
            for ind in range(len(csv_rows)):
                user = row_users[ind]
                row = csv_rows[ind]
                if row['star'] != '':
                    order = models.Order.objects.get_or_create(
                        user=user,
                        product=products[int(row['orderp'])-1],
                        status = int(row['status']),
                        star=int(row['star']),
                        comment=row['comment']
                    )
                else:
                    order = models.Order.objects.get_or_create(
                        user=user,
                        product=products[int(row['orderp'])-1],
                        status = int(row['status']),
                        comment=row['comment']
                    )
                for_save_objects.append(order)


                    
        except Exception as e:
            #transaction.rollback()
            self.stdout.write("data product error:{}".format(e)) 
            failure(e)
        

        

