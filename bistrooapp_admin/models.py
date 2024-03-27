from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    category_sort_id = models.PositiveIntegerField()

    class Meta:
        ordering = ["category_sort_id"]
        verbose_name_plural = "categori_names"

    def __str__(self):
        return self.category_name

class Menuu(models.Model):
    menu_date = models.DateField()
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    price_full = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False,
                                     validators=[MinValueValidator(0,"Väärtus peab olema 0 või 0-st suurem number")])
    price_half = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True,
                                     validators=[MinValueValidator(0,"Väärtus peab olema 0 või 0-st suurem number")])
    is_hided = models.BooleanField(default=False)

    class Meta:
        ordering = ["-menu_date", "category_name", "id"]

    def __str__(self):
        return f'{self.menu_date, self.description}'

class Theme(models.Model):
    menu_date = models.DateField(unique=True)
    theme = models.CharField(max_length=255, blank=True, null=True)
    recommenders = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        ordering = ["-menu_date"]

    def __str__(self):
        return f'{self.theme, self.recommenders, self.author}'

    def clean(self):

        if (self.theme is not None and self.recommenders is None) or (self.recommenders is not None and self.theme is None):
            raise ValidationError( ("Teema ja Soovitajad peavad mõlemad olema täidetud"))
