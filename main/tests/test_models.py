from django.test import TestCase
from django.core.files.images import ImageFile
from main import models

import os.path
from config.settings.development import MEDIA_ROOT 
import logging
logger = logging.getLogger(__name__)

class ModelTest(TestCase):
    
    def setUp(self):
        self.user1 = models.User.objects.create_user("user1", "test-email@gmail.com", "pw432kwjow")
        self.user2 = models.User.objects.create_user("user2", "testt012gg@i.softbank.jp", "12kiwajow")
        self.product = models.Product(
            user=self.user1,
            name="pythonのプログラミングで簡単なwebページ作成を教えます",
            description="webサイトを作成したことがない人に向けて、昨今、機械学習分野でhotなプログラミング言語であるpythonを使用して、webサイトを公開するまで教えます。",
            price=4000,
        )

        self.user1.save()
        self.user2.save()
        self.product.save()
        
    def test_user_model(self):
        url = models.UrlUser.objects.create(
            user=self.user1, 
            name='testホームページ',
            url="http://www.example.co.jp"
        )

        topic = models.interast_Topic_User.objects.create(
            user=self.user1,
            topic_tag="python"
        )
        
        secret_profile = models.SecretProfile.objects.create(
            user=self.user1,
            phone_number='09000001234',
            account_holder="テスト太郎",
            account_number="0123456",
            Deposit_type=10,
            financial_institution_code="0123",
            branch_code="012"
        )
        
        #UseImageに関しては、signals.pyのテストにて確認

        favorite_user = models.FavoriteUser.objects.create(
            user=self.user1,
            target=self.user2,
        )

        block_user = models.BlockUser.objects.create(
            user=self.user1,
            target=self.user2
        )

        self.assertEqual(url.user, self.user1)
        self.assertEqual(topic.user, self.user1)
        self.assertEqual(secret_profile.user, self.user1)
        
        self.assertEqual(favorite_user.user, self.user1)
        self.assertEqual(favorite_user.target, self.user2)
        
        self.assertEqual(block_user.user, self.user1)
        self.assertEqual(block_user.target, self.user2)

        #test get_method
        self.assertEqual(self.user1.get_info(models.UrlUser).count(), 1)
        self.assertEqual(self.user2.get_info(models.UrlUser).count(), 0)
        
        self.assertEqual(self.user1.get_info(models.interast_Topic_User).count(), 1)
        self.assertEqual(self.user1.get_info(models.SecretProfile).count(), 1)
        self.assertEqual(self.user1.get_info(models.FavoriteUser).count(), 1)
        self.assertEqual(self.user1.get_info(models.BlockUser).count(), 1)
        
        """
        for profile in self.user1.get_info(models.SecretProfile):
            print(profile.phone_number)
        """

    
    def test_order_model(self):
        product_tag = models.ProductTag.objects.create(
            name='プログラミングを教えます',
        )

        product_sub_tag1 = models.ProductSubTag.objects.create(name='python') 
        product_sub_tag2 = models.ProductSubTag.objects.create(name='Ruby') 

        self.product.tag = product_tag
        self.product.sub_tags.add(product_sub_tag1)
        self.product.sub_tags.add(product_sub_tag2)

        order = models.Order.objects.create(
            user=self.user2,
            status=10,
            product=self.product,
        )

        order.star = 3
        order.comment = "良かったです"
        
        #お気に入り機能
        favorite_product = models.FavoriteProduct(
            user=self.user1,
            product=self.product
        )

        self.product.save()
        order.save()
        favorite_product.save()

        
        #test Product model
        test_product = self.user1.get_info(models.FavoriteProduct)[0].product
        self.assertEqual(
            test_product, 
            self.product
        )

        self.assertEqual(
            test_product.tag,
            product_tag
        )
        
        self.assertEqual(
            test_product.sub_tags.all()[0], #Many to many
            product_sub_tag1
        )
        
        #test Order model
        self.assertEqual(
            self.user2.get_info(models.Order)[0].user, 
            self.user2
        )

        self.assertEqual(
            self.user2.get_info(models.Order)[0].product.user, 
            self.user1
        )

        #test favorite product model
        self.assertEqual(favorite_product.user, self.user1)

        self.assertEqual(
            self.user1.get_info(models.FavoriteProduct)[0].user, 
            self.user1
        )


    def test_image_model_and_thumbnails_are_generated_on_save(self):
        #user image
        with open("main/fixtures/test_image.jpg", "rb") as f:
            image = models.UserImage(
                user=self.user1,
                image=ImageFile(f, name="tctb.jpg")
            )
        
            with self.assertLogs("main", level="INFO") as cm:
                image.save()
        
        self.assertGreaterEqual(len(cm.output), 1)
        image.refresh_from_db()
        with open(os.path.join(MEDIA_ROOT ,image.thumbnail.name), "rb") as f:
            expected_content = f.read()
            assert image.thumbnail.read() == expected_content

        image.thumbnail.delete(save=False)
        image.image.delete(save=False)

        
        #product image
        with open("main/fixtures/test_image.jpg", "rb") as f:
            image = models.ProductImage(
                product=self.product,
                image=ImageFile(f, name="tctb.jpg")
            )
        
            with self.assertLogs("main", level="INFO") as cm:
                image.save()
        
        self.assertGreaterEqual(len(cm.output), 1)
        image.refresh_from_db()
        with open(os.path.join(MEDIA_ROOT ,image.thumbnail.name), "rb") as f:
            expected_content = f.read()
            
            assert image.thumbnail.read() == expected_content
        image.thumbnail.delete(save=False)
        image.image.delete(save=False)

    


        