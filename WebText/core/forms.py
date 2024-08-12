"""
This file is used to define the forms for the game

HOW TO:
1. Create a new form class for each form you want to create
2. Add the form to the forms.py file
3. Inherit the form from the BasicForm class


This File Does:

1. Defines the BasicForm class
2. Defines the BasicDeleteForm class

"""


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Field, Fieldset, Layout, Submit, HTML
from django import forms
from django.db import models


class BasicForm(forms.Form):
    """FORM to Use in other FORMS"""

    def __init__(self, *args, **kwargs):
        """
        The function initializes a form with specific attributes and layout for a Django model.
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "form w-100"
        self.helper.layout = self.get_layout()

    def get_layout(self):
        """This code snippet is defining a method `get_layout` within the `BaseForm` class.
        The purpose of this method is to dynamically generate a layout for
        the form based on the fields defined in the form class.
        """
        layout = Layout()
        layout.append(HTML(f'<div class="card-header">{self.Meta.verbose_name}</div>'))
        for field_name in self.form_fields():
            layout.append(
                Field(
                    field_name,
                    # placeholder=f"{field.label}",
                    css_class="form-control bg-transparent",
                )
            )
        layout.append(Submit("submit", "Submit", css_class="btn btn-primary"))
        return layout

    def get_initial(self, instance=None):
        ser_data = {}
        for field in self.get_model._meta.fields:
            ser_data[field.name] = getattr(instance, field.name)
        return ser_data

    @classmethod
    def model_fields(cls):
        """Return Fields"""
        return cls.get_model._meta.fields

    @classmethod
    def form_fields(cls):
        """Return Fields"""
        return [field_name for field_name, field in cls.base_fields.items()]

    @classmethod
    @property
    def get_model(cls):
        """Return Model"""
        return cls.Meta.model

    class Meta:
        """SUB META"""
        verbose_name = "Basic Form"
        model = None


class BasicDeleteForm(BasicForm):

    def __init__(self, *args, **kwargs):
        _ = kwargs.pop("instance", None)
        super().__init__(*args, **kwargs)

    def get_layout(self):
        return Layout(Submit("delete", "Delete", css_class="btn btn-primary"))
