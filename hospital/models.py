from django.db import models
from account.models import Account
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.text import slugify

from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField

class City(models.Model):

    cities_list = [
        ("Toshkent","Toshkent"),
        ("Farg'ona","Farg'ona"),
        ("Andijon","Andijon"),
        ("Namangan","Namangan"),
        ("Surxondaryo","Surxondaryo"),
        ("Qashqadaryo","Qashqadaryo"),
        ("Xorazm","Xorazm"),
        ("Navoiy","Navoiy"),
        ("Qoraqalpog'iston Resublikasi","Qoraqalpog'iston Respublikasi"),
        ("Buxoro","Buxoro"),
        ("Toshkent shahri","Toshkent shahri"),
        ("Samarqand","Samarqand"),
    ]

    city_name = models.CharField(max_length=30, choices=cities_list)

    class Meta:
        verbose_name_plural = "City"
    
    def __str__(self):
        return self.city_name
    
class Hospital(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, null=True)
    description = RichTextField()
    address = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Hospital"

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField("Yo'nalish nomi",max_length=100)
    preview_photo = CloudinaryField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Yo'nalish"

    def __str__(self):
        return self.name

class Doctor(models.Model):
    username = models.CharField(max_length=30, unique=True)
    hospital = models.ForeignKey(Hospital, verbose_name='Kasalxonani tanlang:',on_delete=models.CASCADE)
    department = models.ForeignKey(Department, verbose_name="Doktor yo'nalishini tanlang:", on_delete=models.PROTECT)
    first_name = models.CharField('Ismi',max_length=50)
    last_name = models.CharField('Familiyasi',max_length=70)
    slug = models.SlugField(blank=True, null=True, max_length=100)
    description = models.TextField('Doktor haqida ma`lumot',max_length=400)
    preview_photo = CloudinaryField(blank=True)
    work_start_time = models.TimeField('Ishni boshlashnish vaqti')
    work_end_time = models.TimeField('Ishni tugash vaqti')
    sick_list = models.ManyToManyField(Account, blank=True, through='SickItem')
    created_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Doktor"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class SickItem(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, blank=True, null=True)
    weekday = models.DateField(auto_now_add=False, blank=True, null=True)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Kasallar"
        ordering = ['order','-timestamp']


class SicknessList(models.Model):
    name = models.CharField('Kasallik nomi',max_length=120)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    about_sickness = models.TextField('Kasallik haqida ta`rif', blank=True)
    untying = models.TextField(help_text='Ushbu kasallik yuz berganda qanday harakatlarni qilish haqida ta`rif')
    over_18 = models.CharField('18yoshdan yuqori insonlar uchun dori nomi va uning dozasi',max_length=50)
    under_18 = models.CharField('18yoshdan past bolalar uchun dori nomi va uning dozasi',max_length=50)
    photo = CloudinaryField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Sickness List"

    def __str__(self):
        return self.name

class SickAge(models.Model):
    age = models.DateField(auto_now_add=False)


# ---Signals---

@receiver(pre_save, sender=Hospital)
def hospital_signal(instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.city}-{instance.name}")
        instance.save()

@receiver(pre_save, sender=Doctor)
def doctor_signal(instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.hospital.name}-{instance.department.name}-{instance.first_name}-{instance.last_name}")
        instance.save()

@receiver(pre_save, sender=SicknessList)
def save_slug(instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)