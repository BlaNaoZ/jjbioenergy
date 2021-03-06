from accounts.models import Supplier
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
    supplier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'supplier_flag': True}, related_name="Supplier") #Returns the name field of the Supplier instance
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'supplier_flag': False, 'admin': False}, related_name="Customer")

    STEAM_POWER_CHOICE = 'Steam Power Gen'
    ORC_CHOICE = 'ORC'

    EQUIPMENT_CATEGORY_CHOICES = (
        (STEAM_POWER_CHOICE, 'Steam Power Gen'),
        (ORC_CHOICE, 'ORC'),
    )

    equipment_category = models.CharField(max_length=20, choices=EQUIPMENT_CATEGORY_CHOICES, default=STEAM_POWER_CHOICE)

    STAINLESS_STEEL_CHOICE = 'Stainless steel'
    ALLUMINIUM_CHOICE = 'Alluminium'
    HOTEL_CHOICE = 'Hotel'
    SUPERMARKET_CHOICE = 'Supermarket'

    CUSTOMER_PRODUCT_CHOICES = (
        (HOTEL_CHOICE, 'Hotel'),
        (SUPERMARKET_CHOICE, 'Supermarket'),
        (STAINLESS_STEEL_CHOICE, 'Stainless steel'),
        (ALLUMINIUM_CHOICE, 'Alluminium'),
    )

    customer_product = models.CharField(max_length=20, choices=CUSTOMER_PRODUCT_CHOICES, default=STAINLESS_STEEL_CHOICE)
    install_date = models.DateField(default=date.today)
    specification_of_equipment = models.TextField()

    '''
     specification_of_equipment = models.CharField(max_length=200, choices=SPEC_CHOICES, null=True, blank=True)
    '''

    def publish(self):
        self.save()

    def __str__(self):
        return self.reference_number
