from decimal import Decimal
from django.test import TestCase
from main import models

import logging
logger = logging.Logger(__name__)

class ModelTest(TestCase):
    
    def setUp(self):
        self.user1 = models.User.objects.create_user("user1", "test-email@gmail.com", "pw432kwjow")
        self.user2 = models.User.objects.create_user("user2", "testt012gg@i.softbank.jp", "12kiwajow")
        
    def test_user(self):
        
        self.user1.save()

        url = models.UrlUser.objects.create(
            user=self.user1, 
            name='testホームページ',
            user_url="http://www.example.co.jp"
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
            favorite=self.user2,
        )

        block_user = models.BlockUser.objects.create(
            user=self.user1,
            block_user=self.user2
        )

        self.assertEqual(url.user, self.user1)
        self.assertEqual(topic.user, self.user1)
        self.assertEqual(secret_profile.user, self.user1)
        
        self.assertEqual(favorite_user.user, self.user1)
        self.assertEqual(favorite_user.favorite, self.user2)
        
        self.assertEqual(block_user.user, self.user1)
        self.assertEqual(block_user.block_user, self.user2)

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
    

        
        

        