from datetime import datetime
from django import forms
from .models import Theme, Menuu, Category
from django.core.exceptions import ValidationError

class DateInput(forms.DateInput):
    input_type = 'date'
    format = '%d.%m.%Y'

class CurrentDate(forms.Form):
    valitud_kp = forms.DateField(widget=DateInput(attrs={"class": "datepicker-form"}), input_formats=['%d.%m.%Y'], label="")

class DuplicateDate(forms.Form):
    duplikaadi_kp = forms.DateField(widget=DateInput(attrs={"class": "datepicker-form"}),
                                    input_formats=['%d.%m.%Y'], label="Koopia kuupäev", required=True)

class MenuuSearchForm(forms.Form):
    search_phrase = forms.CharField(label="Otsingu fraas",
                                    required=True,
                                    min_length=3,
                                    error_messages={'required': "See väli on kohustuslik.",
                                                    "min_length":"Otsingu fraas peab olema vähemalt 3 tähemärki pikk."})

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category_name", "category_sort_id"]
        labels = {"category_name": "Toidu kategooria", "category_sort_id": "Järjestus nr"}
        error_messages = {"category_name":{"required": "Väli on nõutud"},
                          "category_sort_id":{"required": "Väli on nõutud", "min_value": "Väärtus peab olema 0 või 0-st suurem number"}}


class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ["menu_date", "theme", "recommenders", "author"]
        labels = {"theme": "Teema", "recommenders": "Soovitajad", "author": "Autor"}
        widgets = {
            "menu_date": forms.HiddenInput()
        }

class ThemeUpdateForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ["theme", "recommenders", "author"]
        labels = {"theme": "Teema", "recommenders": "Soovitajad", "author": "Autor"}

class SublineForm(forms.ModelForm):
    class Meta:
        model = Menuu
        fields = ["menu_date", "category_name", "description", "price_full", "price_half"]
        labels = {"description": "Nimetus", "price_full": "Hind suurele", "price_half": "Hind väiksele"}
        widgets = {"menu_date": forms.HiddenInput, "category_name": forms.HiddenInput,
                   "description": forms.Textarea(attrs={"rows": 6})}
        error_messages = {"description": {"required": "Väli on nõutud"},
                          "price_full": {"required": "Väli on nõutud, 0 või 0-st suurem number (0->Prae hinnas)"}}

class SublineUpdateForm(forms.ModelForm):
    class Meta:
        model = Menuu
        fields = ["description", "price_full", "price_half"]
        labels = {"description": "Nimetus", "price_full": "Hind suurele", "price_half": "Hind väiksele"}
        widgets = {"description": forms.Textarea(attrs={"rows": 6})}
        error_messages = {"description": {"required": "Väli on nõutud"},
                          "price_full": {"required": "Väli on nõutud, 0 või 0-st suurem number"}}
