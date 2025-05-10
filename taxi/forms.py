from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple

from taxi.models import Driver, Car


class BaseDriverForm(forms.ModelForm):
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError(
                "Ліцензійний номер має складатись із восьми символів"
            )
        elif not license_number[:3].isupper():
            raise ValidationError(
                "Перші три символи ліцензійного "
                "номера мають бути великими літерами"
            )
        elif not license_number[3:].isdigit():
            raise ValidationError(
                "Останні п'ять символів ліцензійного номера мають бути цифрами"
            )

        return license_number


class LicenseForm(BaseDriverForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class DriverForm(BaseDriverForm):
    class Meta:
        model = Driver
        fields = (
            "password",
            "is_superuser",
            "user_permissions",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
            "license_number",
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
