import json

from django.views import View
from django.http.response import HttpResponse

from main import models

import logging
logger = logging.Logger(__name__)

class FavoriteUserDeleteAjaxView(View):
    """お気に入りのユーザーを削除"""
    def post(self, request, *args, **kwargs):
        body = request.body.decode('utf-8')
        bjson = json.loads(body)
        login_user = bjson['login_user'] 
        target = bjson['target']
        try:
            delete_obj = models.FavoriteUser.objects.filter(user__username=login_user).filter(target__username=target)
            delete_obj.delete()
        except Exception as e:
            logger.error(e)
            data = {
                'success': False,
                'message': 'Can not Create favorite user'
            }
            data_json = json.dumps(data)
            return HttpResponse(data_json, content_type='application/json')
        data = {
            'success': True,
            'message': 'test delete',
        }
        data_json = json.dumps(data)
        return HttpResponse(data_json, content_type='application/json')

class FavoriteUserCreateAjaxView(View):
    """お気に入りのユーザーを削除"""
    def post(self, request, *args, **kwargs):
        body = request.body.decode('utf-8')
        bjson = json.loads(body)
        login_user = bjson['login_user'] 
        target = bjson['target']

        try:
            login_user_obj = models.User.objects.filter(username=login_user)[0]
            target_user_obj = models.User.objects.filter(username=target)[0]
            favorite_user_obj = models.FavoriteUser(
                user=login_user_obj, target=target_user_obj
            )
            favorite_user_obj.save()
        except Exception as e:
            logger.error(e)
            data = {
                'success': False,
                'message': 'Can not Create favorite user'
            }
            data_json = json.dumps(data)
            return HttpResponse(data_json, content_type='application/json')


        data = {
            'success': True,
            'message': 'test create',
        }
        data_json = json.dumps(data)
        return HttpResponse(data_json, content_type='application/json')

class FavoriteProductDeleteAjaxView(View):
    """お気に入りのユーザーを削除"""
    def post(self, request, *args, **kwargs):
        body = request.body.decode('utf-8')
        bjson = json.loads(body)
        login_user = bjson['login_user'] 
        target = bjson['target']
        try:
            delete_obj = models.FavoriteProduct.objects.filter(user__username=login_user).filter(product__uuid_url=target)
            delete_obj.delete()
        except Exception as e:
            logger.error(e)
            data = {
                'success': False,
                'message': 'Can not Create favorite product'
            }
            data_json = json.dumps(data)
            return HttpResponse(data_json, content_type='application/json')
        data = {
            'success': True,
            'message': 'test delete',
        }
        data_json = json.dumps(data)
        return HttpResponse(data_json, content_type='application/json')

class FavoriteProductCreateAjaxView(View):
    """お気に入りのユーザーを削除"""
    def post(self, request, *args, **kwargs):
        body = request.body.decode('utf-8')
        bjson = json.loads(body)
        login_user = bjson['login_user'] 
        target = bjson['target']

        try:
            login_user_obj = models.User.objects.filter(username=login_user)[0]
            target_product_obj = models.Product.objects.filter(uuid_url=target)[0]
            favorite_product_obj = models.FavoriteProduct(
                user=login_user_obj, product=target_product_obj
            )
            favorite_product_obj.save()
        except Exception as e:
            logger.error(e)
            data = {
                'success': False,
                'message': 'Can not Create favorite product'
            }
            data_json = json.dumps(data)
            return HttpResponse(data_json, content_type='application/json')

    
        data = {
            'success': True,
            'message': 'test create',
        }
        data_json = json.dumps(data)
        return HttpResponse(data_json, content_type='application/json')