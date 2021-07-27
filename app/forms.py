from django import forms

from .models import Reference


class DateInput(forms.DateInput):
    input_type = 'date'


class ReferenceForm(forms.ModelForm):

    class Meta:
        model = Reference
        fields = ('equipment_category', 'customer', 'customer_product', 'install_date', 'specification_of_equipment',)
        widgets = {
            'install_date': DateInput()
        }