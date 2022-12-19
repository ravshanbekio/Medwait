from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.conf import settings
from django.utils.text import slugify

@receiver(pre_save, sender=settings.DOCTOR_MODEL)
def doctor_signal(instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.hospital.name} {instance.first_name} {instance.last_name}")
        instance.save()