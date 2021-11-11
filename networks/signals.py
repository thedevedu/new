from django.db.models.signals import pre_save

from .models import Network
from nanoid import generate

# @receiver(post_save, sender=Profile)

def createId(sender, instance, **kwargs):
    network = instance
    network.id = generate(size=12)

pre_save.connect(createId, sender=Network)