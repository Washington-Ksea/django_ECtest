from django.core.files.base import ContentFile
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import UserImage, ProductImage

from io import BytesIO
from PIL import Image
import logging
logger = logging.Logger(__name__)

THUMBNAIL_SIZE = (300, 300)

def generate_thumbnail_process(instance):
    image = Image.open(instance.image)
    image = image.convert('RGB')    
    image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

    temp_thumb = BytesIO()
    image.save(temp_thumb, "JPEG")
    temp_thumb.seek(0)
    
    logger.debug("#create thumbnail name: {}".format(instance.image.name))
    instance.thumbnail.save(
        instance.image.name, 
        ContentFile(temp_thumb.read()),
        save=False
    )
    temp_thumb.close()

@receiver(pre_save, sender=UserImage)
def user_generate_thumbnail(sender, instance, **kwargs):
    logger.debug("Generating thumbnail for user {}".format(instance.user.id))
    generate_thumbnail_process(instance)


@receiver(pre_save, sender=ProductImage)
def product_generate_thumbnail(sender, instance, **kwargs):
    logger.debug("Generating thumbnail for prduct {}".format(instance.product.id))
    generate_thumbnail_process(instance)

