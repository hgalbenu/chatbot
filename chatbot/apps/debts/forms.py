from django.forms.models import ModelForm

from .models import Debt


class DebtForm(ModelForm):
    class Meta:
        model = Debt
        exclude = (
            'id',
            'user_profile',
        )
