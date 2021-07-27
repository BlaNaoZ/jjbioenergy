from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django import forms
from django.utils.datetime_safe import date

'''SPEC_CHOICES = (
    ('cap', 'capacity'),
    ('hs', 'heat source'),
    ('hst', 'heat source temperature'),
    ('size', 'size'),
    ('w', 'weight'),
)
'''
'''class ListTextWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list': 'list__%s' % self._name})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">' % item
        data_list += '</datalist>'

        return (text_html + data_list)
'''


class Reference(models.Model):
    reference_number = models.CharField(max_length=50)
    equipment_category = models.CharField(max_length=20)
    supplier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    customer = models.CharField(max_length=50)
    customer_product = models.CharField(max_length=100)
    install_date = models.DateField(default=date.today)
    specification_of_equipment = models.TextField()

    '''
     specification_of_equipment = models.CharField(max_length=200, choices=SPEC_CHOICES, null=True, blank=True)
    '''

    def publish(self):
        self.save()

    def __str__(self):
        return self.reference_number


class Profile(models.Model):
    STUDENT = 1
    TEACHER = 2
    SUPERVISOR = 3
    ROLE_CHOICES = (
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
        (SUPERVISOR, 'Supervisor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
